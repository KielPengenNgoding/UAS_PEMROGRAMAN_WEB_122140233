from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPForbidden, HTTPUnprocessableEntity
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from datetime import datetime, date
from marshmallow import ValidationError
import logging
import re

from ..orms.user import UserORM
from ..orms.court import CourtORM
from ..orms.booking import BookingORM
from ..schemas.booking import BookingSchema

log = logging.getLogger(__name__)

@view_defaults(route_name='booking')
class BookingViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        user_id = int(self.request.matchdict['user_id'])
        # Verify user exists
        user = self.request.dbsession.query(UserORM).filter(UserORM.id == user_id).first()
        if user is None:
            return HTTPNotFound(detail='User not found')
        
        # Periksa otorisasi: hanya user sendiri atau admin yang boleh melihat booking
        current_user_id = self.request.authenticated_userid
        current_user = None
        if current_user_id:
            current_user = self.request.dbsession.query(UserORM).filter(UserORM.id == current_user_id).first()
        
        # Jika bukan admin dan bukan user sendiri, tolak akses
        if current_user and current_user.role != 'admin' and str(current_user.id) != str(user_id):
            return HTTPForbidden(detail='You do not have permission to view these bookings')
            
        # Use joinedload to load court information with bookings
        bookings = self.request.dbsession.query(BookingORM).options(
            joinedload(BookingORM.court)
        ).filter(BookingORM.user_id == user_id).all()
        return {
            'data': [self._booking_to_dict(booking) for booking in bookings],
            'total': len(bookings)
        }

    @view_config(request_method='POST', renderer='json')
    def add(self):
        try:
            # Ekstrak user_id dari URL
            try:
                user_id = int(self.request.matchdict['user_id'])
                log.info(f"Received booking request for user {user_id}")
                log.info(f"Request body: {self.request.json_body}")
            except (ValueError, KeyError) as e:
                log.error(f"Invalid user_id in URL: {str(e)}")
                return HTTPBadRequest(detail='Invalid user ID')
            
            # Verify user exists - wrap in try/except untuk menangani error database
            try:
                user = self.request.dbsession.query(UserORM).filter(UserORM.id == user_id).first()
                if user is None:
                    log.error(f"User {user_id} not found")
                    return HTTPNotFound(detail='User not found')
            except Exception as e:
                log.error(f"Database error when querying user: {str(e)}")
                return HTTPBadRequest(detail='Error accessing user data')
                
            # Periksa otorisasi: hanya user sendiri atau admin yang boleh membuat booking
            try:
                current_user_id = self.request.authenticated_userid
                current_user = None
                if current_user_id:
                    current_user = self.request.dbsession.query(UserORM).filter(UserORM.id == current_user_id).first()
                
                # Jika bukan admin dan bukan user sendiri, tolak akses
                if current_user and current_user.role != 'admin' and str(current_user.id) != str(user_id):
                    log.error(f"User {current_user_id} tried to create booking for user {user_id}")
                    return HTTPForbidden(detail='You do not have permission to create bookings for this user')
            except Exception as e:
                log.error(f"Error checking authorization: {str(e)}")
                return HTTPBadRequest(detail='Error checking authorization')
            
            try:
                # Inisialisasi schema dan atur berdasarkan metode HTTP
                schema = BookingSchema()
                schema.set_schema_by_method('POST')
                
                # Validasi dan deserialisasi input
                request_data = self.request.json_body.copy()
                request_data['user_id'] = user_id  # Pastikan user_id dari URL digunakan
                
                # Log data sebelum validasi untuk debugging
                log.info(f"Raw request data: {request_data}")
                log.info(f"booking_date type: {type(request_data.get('booking_date', None))}")
                log.info(f"time_slot value: {request_data.get('time_slot', None)}")
                
                # Pastikan format booking_date benar (string ISO format)
                if 'booking_date' in request_data and isinstance(request_data['booking_date'], str):
                    try:
                        # Coba parsing tanggal untuk memastikan format valid
                        parsed_date = datetime.strptime(request_data['booking_date'], '%Y-%m-%d').date()
                        log.info(f"Successfully parsed booking_date: {parsed_date}")
                        # Gunakan string asli untuk validasi schema
                    except ValueError as e:
                        log.error(f"Invalid date format: {request_data['booking_date']}, error: {str(e)}")
                        return HTTPBadRequest(detail=f"Invalid date format. Expected YYYY-MM-DD, got: {request_data['booking_date']}")
                
                # Pastikan format time_slot benar
                if 'time_slot' in request_data and isinstance(request_data['time_slot'], str):
                    # Validasi format time_slot secara manual
                    time_slot_pattern = r'^([01]?[0-9]|2[0-3])\.00 - ([01]?[0-9]|2[0-3])\.00$'
                    if not re.match(time_slot_pattern, request_data['time_slot']):
                        log.error(f"Invalid time_slot format: {request_data['time_slot']}")
                        return HTTPBadRequest(detail=f"Invalid time slot format. Expected 'HH.00 - HH.00', got: {request_data['time_slot']}")
                
                log.info(f"Validating data: {request_data}")
            except Exception as e:
                log.error(f"Error processing request data: {str(e)}")
                return HTTPBadRequest(detail=f"Error processing request data: {str(e)}")
            
            try:
                validated_data = schema.load(request_data)
                log.info(f"Validation successful. Validated data: {validated_data}")
            except ValidationError as e:
                log.error(f"Validation error: {e.messages}")
                return HTTPUnprocessableEntity(detail={'validation_errors': e.messages})
            except Exception as e:
                log.error(f"Unexpected validation error: {str(e)}")
                return HTTPBadRequest(detail=f"Error validating data: {str(e)}")
            
            try:
                # Verify court exists
                court_id = validated_data['court_id']
                court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
                if court is None:
                    log.error(f"Court {court_id} not found")
                    return HTTPNotFound(detail='Court not found')
                    
                # Check if there's already a booking for this court, date, and time slot
                booking_date = validated_data['booking_date']
                time_slot = validated_data['time_slot']
                
                log.info(f"Checking for existing bookings: court_id={court_id}, date={booking_date}, time_slot={time_slot}")
                
                existing_booking = self.request.dbsession.query(BookingORM).filter(
                    BookingORM.court_id == court_id,
                    BookingORM.booking_date == booking_date,
                    BookingORM.time_slot == time_slot,
                    BookingORM.status != 'cancelled'  # Ignore cancelled bookings
                ).first()
                
                if existing_booking:
                    log.error(f"Booking conflict: Court {court_id} already booked on {booking_date} at {time_slot}")
                    return HTTPBadRequest(detail='This court is already booked for the selected date and time slot')
            except Exception as e:
                log.error(f"Error checking court availability: {str(e)}")
                return HTTPBadRequest(detail=f"Error checking court availability: {str(e)}")
            
            try:
                # Buat booking baru dengan data yang sudah divalidasi
                new_booking = BookingORM(
                    user_id=user_id,
                    court_id=court_id,
                    booking_date=validated_data['booking_date'],
                    time_slot=validated_data['time_slot'],
                    full_name=validated_data.get('full_name', user.full_name),
                    phone_number=validated_data['phone_number'],
                    status=validated_data.get('status', 'pending')
                )
                
                log.info(f"Creating new booking: {new_booking.__dict__}")
                
                self.request.dbsession.add(new_booking)
                self.request.dbsession.flush()
            except Exception as e:
                log.error(f"Error creating booking: {str(e)}")
                # Pastikan transaksi di-rollback
                self.request.tm.abort()
                return HTTPBadRequest(detail=f"Error creating booking: {str(e)}")
            
            log.info(f"Booking created successfully with ID {new_booking.id}")
            return {'message': 'Booking added successfully', 'id': new_booking.id}
        except ValidationError as e:
            # Tangani error validasi dari Marshmallow
            log.error(f"Validation error: {e.messages}")
            # Pastikan transaksi di-rollback
            try:
                self.request.tm.abort()
            except Exception as abort_error:
                log.error(f"Error aborting transaction: {str(abort_error)}")
            return HTTPUnprocessableEntity(detail={'validation_errors': e.messages})
        except ValueError as e:
            log.error(f"Value error: {str(e)}")
            # Pastikan transaksi di-rollback
            try:
                self.request.tm.abort()
            except Exception as abort_error:
                log.error(f"Error aborting transaction: {str(abort_error)}")
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')
        except IntegrityError as e:
            log.error(f"Integrity error: {str(e)}")
            # Pastikan transaksi di-rollback
            try:
                self.request.tm.abort()
            except Exception as abort_error:
                log.error(f"Error aborting transaction: {str(abort_error)}")
            return HTTPBadRequest(detail='A booking conflict exists')
        except Exception as e:
            log.error(f"Unexpected error: {str(e)}")
            # Pastikan transaksi di-rollback
            try:
                self.request.tm.abort()
            except Exception as abort_error:
                log.error(f"Error aborting transaction: {str(abort_error)}")
            return HTTPBadRequest(detail=str(e))

    def _booking_to_dict(self, booking):
        return {
            'id': booking.id,
            'user_id': booking.user_id,
            'court_id': booking.court_id,
            'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
            'time_slot': booking.time_slot,
            'full_name': booking.full_name,
            'phone_number': booking.phone_number,
            'status': booking.status
        }

@view_defaults(route_name='booking_detail')
class BookingDetailViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def detail(self):
        booking_id = int(self.request.matchdict['id'])
        user_id = int(self.request.matchdict['user_id'])
        
        # Periksa otorisasi: hanya user sendiri atau admin yang boleh melihat detail booking
        current_user_id = self.request.authenticated_userid
        current_user = None
        if current_user_id:
            current_user = self.request.dbsession.query(UserORM).filter(UserORM.id == current_user_id).first()
        
        # Jika bukan admin dan bukan user sendiri, tolak akses
        if current_user and current_user.role != 'admin' and str(current_user.id) != str(user_id):
            return HTTPForbidden(detail='You do not have permission to view this booking')
        
        booking = self.request.dbsession.query(BookingORM).filter(
            BookingORM.id == booking_id,
            BookingORM.user_id == user_id
        ).first()
        
        if booking is None:
            return HTTPNotFound(detail='Booking not found')
        
        return self._booking_to_dict(booking)

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            booking_id = int(self.request.matchdict['id'])
            user_id = int(self.request.matchdict['user_id'])
            
            # Periksa otorisasi
            current_user_id = self.request.authenticated_userid
            current_user = None
            if current_user_id:
                current_user = self.request.dbsession.query(UserORM).filter(UserORM.id == current_user_id).first()
            
            booking = self.request.dbsession.query(BookingORM).filter(
                BookingORM.id == booking_id,
                BookingORM.user_id == user_id
            ).first()
            
            if booking is None:
                return HTTPNotFound(detail='Booking not found')
                
            # Jika bukan admin dan bukan user sendiri, tolak akses
            if current_user and current_user.role != 'admin' and str(current_user.id) != str(user_id):
                return HTTPForbidden(detail='You do not have permission to update this booking')
                
            # Jika user biasa mencoba mengubah status, tolak akses
            if current_user and current_user.role != 'admin' and 'status' in self.request.json_body:
                return HTTPForbidden(detail='Only admin can change booking status')
            
            # Inisialisasi schema dan atur berdasarkan metode HTTP
            schema = BookingSchema()
            schema.set_schema_by_method('PUT')  # Ini akan membuat semua field menjadi opsional
            
            # Validasi dan deserialisasi input
            request_data = self.request.json_body.copy()
            request_data['user_id'] = user_id  # Pastikan user_id dari URL digunakan
            validated_data = schema.load(request_data)
            
            # Update booking dengan data yang sudah divalidasi
            if 'court_id' in validated_data:
                court_id = validated_data['court_id']
                court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
                if court is None:
                    return HTTPNotFound(detail='Court not found')
                booking.court_id = court_id
            
            if 'booking_date' in validated_data:
                booking.booking_date = validated_data['booking_date']
                
            if 'time_slot' in validated_data:
                booking.time_slot = validated_data['time_slot']
                
            if 'full_name' in validated_data:
                booking.full_name = validated_data['full_name']
            if 'phone_number' in validated_data:
                booking.phone_number = validated_data['phone_number']
            if 'status' in validated_data:
                booking.status = validated_data['status']
            
            self.request.dbsession.flush()
            return {'message': 'Booking updated successfully', 'id': booking.id}
        except ValidationError as e:
            # Tangani error validasi dari Marshmallow
            return HTTPUnprocessableEntity(detail={'validation_errors': e.messages})
        except ValueError as e:
            return HTTPBadRequest(detail=f'Invalid value: {str(e)}')
        except IntegrityError:
            return HTTPBadRequest(detail='Update would violate unique constraints')

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        booking_id = int(self.request.matchdict['id'])
        user_id = int(self.request.matchdict['user_id'])
        
        # Periksa otorisasi
        current_user_id = self.request.authenticated_userid
        current_user = None
        if current_user_id:
            current_user = self.request.dbsession.query(UserORM).filter(UserORM.id == current_user_id).first()
        
        # Jika bukan admin dan bukan user sendiri, tolak akses
        if current_user and current_user.role != 'admin' and str(current_user.id) != str(user_id):
            return HTTPForbidden(detail='You do not have permission to delete this booking')
        
        booking = self.request.dbsession.query(BookingORM).filter(
            BookingORM.id == booking_id,
            BookingORM.user_id == user_id
        ).first()
        
        if booking is None:
            return HTTPNotFound(detail='Booking not found')
        
        self.request.dbsession.delete(booking)
        return {'message': 'Booking deleted successfully', 'id': booking_id}
    
    def _booking_to_dict(self, booking):
        return {
            'id': booking.id,
            'user_id': booking.user_id,
            'court_id': booking.court_id,
            'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
            'time_slot': booking.time_slot,
            'full_name': booking.full_name,
            'phone_number': booking.phone_number,
            'status': booking.status
        }

@view_defaults(route_name='court_booking')
class CourtBookingViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        court_id = int(self.request.matchdict['court_id'])
        # Verify court exists
        court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
        if court is None:
            return HTTPNotFound(detail='Court not found')
            
        # Get all bookings for this court that are not cancelled
        bookings = self.request.dbsession.query(BookingORM).filter(
            BookingORM.court_id == court_id,
            BookingORM.status != 'cancelled'
        ).all()
        
        return {
            'data': [self._booking_to_dict(booking) for booking in bookings],
            'total': len(bookings)
        }
        
    def _booking_to_dict(self, booking):
        return {
            'id': booking.id,
            'user_id': booking.user_id,
            'court_id': booking.court_id,
            'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
            'time_slot': booking.time_slot,
            'full_name': booking.full_name,
            'phone_number': booking.phone_number,
            'status': booking.status
        }

@view_defaults(route_name='all_bookings')
class AllBookingsViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        # Get all active bookings (not cancelled)
        bookings = self.request.dbsession.query(BookingORM).filter(
            BookingORM.status != 'cancelled'
        ).all()
        
        return {
            'data': [self._booking_to_dict(booking) for booking in bookings],
            'total': len(bookings)
        }
        
    def _booking_to_dict(self, booking):
        return {
            'id': booking.id,
            'user_id': booking.user_id,
            'court_id': booking.court_id,
            'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
            'time_slot': booking.time_slot,
            'full_name': booking.full_name,
            'phone_number': booking.phone_number,
            'status': booking.status
        }
