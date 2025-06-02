from pyramid.view import view_config, view_defaults
from ..orms.court import CourtORM
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPUnprocessableEntity, HTTPForbidden
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from ..schemas.court import CourtSchema
import logging
import os
from sqlalchemy.orm import Session
from ..models.court import Court
from ..models.booking import Booking
from ..utils.file_upload import save_uploaded_file
import shutil

log = logging.getLogger(__name__)

@view_defaults(route_name='admin_courts', permission='admin')
class AdminCourtViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        query = self.request.dbsession.query(CourtORM)
        
        # Get filter parameters from query string
        category = self.request.params.get('category')
        status = self.request.params.get('status')
        
        # Apply filters if provided
        if category:
            query = query.filter(CourtORM.court_category == category)
        if status:
            query = query.filter(CourtORM.status == status)
            
        courts = query.all()
        
        # Get unique categories for filter options
        categories = self.request.dbsession.query(CourtORM.court_category).distinct().all()
        categories = [cat[0] for cat in categories]
        
        return {
            'data': [self._court_to_dict(court) for court in courts],
            'total': len(courts),
            'categories': categories,
            'statuses': ['available', 'maintenance', 'booked']  # Fixed list of possible statuses
        }
    
    @view_config(request_method='POST', renderer='json')
    def add(self):
        # Log informasi tentang request untuk debugging
        log.info(f"User attempting to add court.")
        log.info(f"Request principals: {self.request.effective_principals}")
        
        # Permission check sudah dilakukan oleh Pyramid berdasarkan view_defaults(permission='admin')
        # sehingga kita tidak perlu melakukan pengecekan manual lagi
            
        try:
            # Inisialisasi schema dan atur berdasarkan metode HTTP
            schema = CourtSchema()
            schema.set_schema_by_method('POST')
            
            # Validasi dan deserialisasi input
            validated_data = schema.load(self.request.json_body)
            
            # Buat court baru dengan data yang sudah divalidasi
            new_court = CourtORM(
                court_name=validated_data['court_name'],
                court_category=validated_data['court_category'],
                description=validated_data.get('description', ''),
                status=validated_data.get('status', 'available'),
                image_url=validated_data.get('image_url')
            )
            self.request.dbsession.add(new_court)
            self.request.dbsession.flush()
            
            return {
                'status': 'success',
                'message': 'Court added successfully', 
                'court': self._court_to_dict(new_court)
            }
        except ValidationError as e:
            # Tangani error validasi dari Marshmallow
            return HTTPUnprocessableEntity(json={
                'status': 'error',
                'message': 'Validation error',
                'errors': e.messages
            })
        except IntegrityError:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': 'A court with this name already exists'
            })
        except Exception as e:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': str(e)
            })
    
    def _court_to_dict(self, court):
        return {
            'id_court': court.id_court,
            'court_name': court.court_name,
            'court_category': court.court_category,
            'description': court.description,
            'status': court.status,
            'image_url': court.image_url
        }

@view_defaults(route_name='admin_court_detail', permission='admin')
class AdminCourtDetailViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def detail(self):
        court_id = int(self.request.matchdict['id_court'])
        court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
        if court is None:
            return HTTPNotFound(json={
                'status': 'error',
                'message': 'Court not found'
            })
        return {
            'status': 'success',
            'court': self._court_to_dict(court)
        }

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            court_id = int(self.request.matchdict['id_court'])
            court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
            if court is None:
                return HTTPNotFound(json={
                    'status': 'error',
                    'message': 'Court not found'
                })
            
            # Inisialisasi schema dan atur berdasarkan metode HTTP
            schema = CourtSchema()
            schema.set_schema_by_method('PUT')  # Ini akan membuat semua field menjadi opsional
            
            # Validasi dan deserialisasi input
            validated_data = schema.load(self.request.json_body)
            
            # Update court dengan data yang sudah divalidasi
            if 'court_name' in validated_data:
                court.court_name = validated_data['court_name']
            if 'court_category' in validated_data:
                court.court_category = validated_data['court_category']
            if 'description' in validated_data:
                court.description = validated_data['description']
            if 'status' in validated_data:
                court.status = validated_data['status']
            if 'image_url' in validated_data:
                court.image_url = validated_data['image_url']
            
            self.request.dbsession.flush()
            return {
                'status': 'success',
                'message': 'Court updated successfully',
                'court': self._court_to_dict(court)
            }
        except ValidationError as e:
            # Tangani error validasi dari Marshmallow
            return HTTPUnprocessableEntity(json={
                'status': 'error',
                'message': 'Validation error',
                'errors': e.messages
            })
        except IntegrityError:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': 'Update would violate unique constraints'
            })
        except Exception as e:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': str(e)
            })

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        try:
            court_id = int(self.request.matchdict['id_court'])
            court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
            if court is None:
                return HTTPNotFound(json={
                    'status': 'error',
                    'message': 'Court not found'
                })
            
            # Cek apakah ada booking yang terkait dengan court ini
            from ..orms.booking import BookingORM
            bookings = self.request.dbsession.query(BookingORM).filter(
                BookingORM.court_id == court_id
            ).count()
            
            if bookings > 0:
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': f'Cannot delete court with {bookings} active bookings. Cancel or delete the bookings first.'
                })
            
            self.request.dbsession.delete(court)
            return {
                'status': 'success',
                'message': 'Court deleted successfully',
                'id_court': court_id
            }
        except Exception as e:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': str(e)
            })
    
    def _court_to_dict(self, court):
        return {
            'id_court': court.id_court,
            'court_name': court.court_name,
            'court_category': court.court_category,
            'description': court.description,
            'status': court.status,
            'image_url': court.image_url
        }

@view_defaults(route_name='admin_court_upload_image', permission='admin')
class AdminCourtUploadViews:
    def __init__(self, request):
        self.request = request
    
    @view_config(request_method='POST', renderer='json')
    def upload_image(self):
        try:
            log.info("Processing image upload request")
            log.info(f"Request method: {self.request.method}")
            log.info(f"Content-Type: {self.request.content_type}")
            log.info(f"Request headers: {dict(self.request.headers)}")
            
            court_id = int(self.request.matchdict['id_court'])
            log.info(f"Court ID: {court_id}")
            
            court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
            if court is None:
                log.error(f"Court not found with ID: {court_id}")
                return HTTPNotFound(json={
                    'status': 'error',
                    'message': 'Court not found'
                })
            
            # Pastikan request adalah multipart form
            if not self.request.POST:
                log.error("Request is not multipart form data")
                log.info(f"Request body: {self.request.body[:200]}...")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': 'Expected multipart form data'
                })
            
            log.info(f"POST data keys: {list(self.request.POST.keys())}")
            
            # Dapatkan file yang diupload
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'courts')
            log.info(f"Upload directory: {upload_dir}")
            
            # Pastikan direktori upload ada
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir, exist_ok=True)
                log.info(f"Created upload directory: {upload_dir}")
                
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            log.info(f"Allowed extensions: {allowed_extensions}")
            
            # Cek apakah 'image' ada di request.POST
            if 'image' not in self.request.POST:
                log.error("No 'image' field found in the request")
                log.info(f"Available fields: {list(self.request.POST.keys())}")
                
                # Check if the image might be in the request.POST.items
                for key in self.request.POST.keys():
                    log.info(f"Field {key} type: {type(self.request.POST[key])}")
                    if hasattr(self.request.POST[key], 'filename'):
                        log.info(f"Found file-like object in field: {key}")
                
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': "No 'image' field found in the request"
                })
            
            image_url = save_uploaded_file(
                request=self.request,
                field_name='image',
                upload_dir=upload_dir,
                allowed_extensions=allowed_extensions
            )
            
            if not image_url:
                log.error("Failed to upload image")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': 'Failed to upload image. Make sure it is a valid image file (jpg, jpeg, png, gif).'
                })
            
            # Update image_url di database
            log.info(f"Updating court {court_id} with image URL: {image_url}")
            court.image_url = image_url
            self.request.dbsession.flush()
            
            return {
                'status': 'success',
                'message': 'Image uploaded successfully',
                'court': self._court_to_dict(court)
            }
        except Exception as e:
            log.error(f"Error uploading image: {str(e)}")
            import traceback
            log.error(traceback.format_exc())
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Error uploading image: {str(e)}'
            })
    
    def _court_to_dict(self, court):
        return {
            'id_court': court.id_court,
            'court_name': court.court_name,
            'court_category': court.court_category,
            'description': court.description,
            'status': court.status,
            'image_url': court.image_url
        }

@view_defaults(route_name='admin_upload_image', permission='admin')
class AdminUploadImageView:
    def __init__(self, request):
        self.request = request
    
    @view_config(request_method='POST', renderer='json')
    def upload_image(self):
        try:
            log.info("Processing image upload request")
            
            # Pastikan request adalah multipart form
            if not self.request.POST:
                log.error("Request is not multipart form data")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': 'Expected multipart form data'
                })
            
            # Dapatkan file yang diupload
            if 'image' not in self.request.POST:
                log.error("No 'image' field found in the request")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': "No 'image' field found in the request"
                })

            # Dapatkan nama file yang diinginkan
            filename = self.request.POST.get('filename')
            if not filename:
                log.error("No 'filename' field found in the request")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': "No 'filename' specified"
                })

            # Validasi ekstensi file
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in allowed_extensions:
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': f'File extension not allowed. Use: {", ".join(allowed_extensions)}'
                })

            # Set path untuk menyimpan file
            frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend_lapangan', 'public', 'images')
            file_path = os.path.join(frontend_path, filename)

            # Pastikan direktori ada
            os.makedirs(frontend_path, exist_ok=True)

            # Simpan file
            file_obj = self.request.POST['image'].file
            with open(file_path, 'wb') as output_file:
                shutil.copyfileobj(file_obj, output_file)

            return {
                'status': 'success',
                'message': 'Image uploaded successfully',
                'filename': filename
            }

        except Exception as e:
            log.error(f"Error uploading image: {str(e)}")
            import traceback
            log.error(traceback.format_exc())
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Error uploading image: {str(e)}'
            })
