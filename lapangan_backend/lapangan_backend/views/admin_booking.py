from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPForbidden, HTTPUnprocessableEntity
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from marshmallow import ValidationError
import logging

from ..orms.user import UserORM
from ..orms.court import CourtORM
from ..orms.booking import BookingORM
from ..schemas.booking import BookingSchema

log = logging.getLogger(__name__)

@view_defaults(route_name='admin_bookings', permission='admin')
class AdminBookingViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def list(self):
        # Buat transaksi baru untuk operasi ini
        import transaction
        with transaction.manager:
            try:
                log.info("Admin fetching all bookings")
                # Admin dapat melihat semua booking
                try:
                    bookings = self.request.dbsession.query(BookingORM).all()
                    log.info(f"Found {len(bookings)} bookings")
                    
                    result_data = []
                    for booking in bookings:
                        try:
                            booking_dict = self._booking_to_dict(booking)
                            result_data.append(booking_dict)
                        except Exception as e:
                            log.error(f"Error processing booking {booking.id if hasattr(booking, 'id') else 'unknown'}: {str(e)}")
                            # Skip this booking but continue with others
                            continue
                            
                    return {
                        'data': result_data,
                        'total': len(result_data)
                    }
                except Exception as e:
                    log.error(f"Database error when fetching bookings: {str(e)}")
                    # Mark transaction for abort
                    transaction.abort()
                    return {
                        'data': [],
                        'total': 0,
                        'error': 'Error fetching bookings data'
                    }
            except Exception as e:
                log.error(f"Unexpected error in admin bookings list: {str(e)}")
                # Mark transaction for abort
                transaction.abort()
                return {
                    'data': [],
                    'total': 0,
                    'error': 'Unexpected error'
                }
    
    def _booking_to_dict(self, booking):
        try:
            # Get court name for the booking
            court_name = "Unknown Court"
            try:
                court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == booking.court_id).first()
                if court:
                    court_name = court.court_name
            except Exception as e:
                log.error(f"Error fetching court data for booking {booking.id}: {str(e)}")
            
            # Get user information
            user_email = "Unknown User"
            try:
                user = self.request.dbsession.query(UserORM).filter(UserORM.id == booking.user_id).first()
                if user:
                    user_email = user.email
            except Exception as e:
                log.error(f"Error fetching user data for booking {booking.id}: {str(e)}")
            
            return {
                'id': booking.id,
                'user_id': booking.user_id,
                'user_email': user_email,
                'court_id': booking.court_id,
                'court_name': court_name,
                'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
                'time_slot': booking.time_slot,
                'full_name': booking.full_name,
                'phone_number': booking.phone_number,
                'status': booking.status
            }
        except Exception as e:
            log.error(f"Error in _booking_to_dict: {str(e)}")
            # Return minimal booking data to avoid breaking the API response
            return {
                'id': getattr(booking, 'id', 'unknown'),
                'status': getattr(booking, 'status', 'unknown'),
                'error': 'Error processing booking data'
            }

@view_defaults(route_name='admin_booking_detail', permission='admin')
class AdminBookingDetailViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def detail(self):
        try:
            booking_id = int(self.request.matchdict['id'])
            try:
                booking = self.request.dbsession.query(BookingORM).filter(BookingORM.id == booking_id).first()
                
                if booking is None:
                    return HTTPNotFound(json={
                        'status': 'error',
                        'message': 'Booking not found'
                    })
                    
                return {
                    'status': 'success',
                    'booking': self._booking_to_dict(booking)
                }
            except Exception as e:
                log.error(f"Database error when fetching booking details: {str(e)}")
                # Rollback transaction if needed
                try:
                    self.request.tm.abort()
                except Exception as abort_error:
                    log.error(f"Error aborting transaction: {str(abort_error)}")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': f'Error fetching booking details: {str(e)}'
                })
        except ValueError as e:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Invalid booking ID: {str(e)}'
            })
        except Exception as e:
            log.error(f"Unexpected error in booking detail: {str(e)}")
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            })

    @view_config(request_method='PUT', renderer='json')
    def update(self):
        try:
            booking_id = int(self.request.matchdict['id'])
            try:
                booking = self.request.dbsession.query(BookingORM).filter(BookingORM.id == booking_id).first()
                
                if booking is None:
                    return HTTPNotFound(json={
                        'status': 'error',
                        'message': 'Booking not found'
                    })
                    
                # Inisialisasi schema dan atur berdasarkan metode HTTP
                schema = BookingSchema()
                schema.set_schema_by_method('PUT')
                
                # Validasi dan deserialisasi input
                validated_data = schema.load(self.request.json_body)
                
                # Update booking dengan data yang sudah divalidasi
                if 'court_id' in validated_data:
                    court_id = validated_data['court_id']
                    try:
                        court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == court_id).first()
                        if court is None:
                            return HTTPNotFound(json={
                                'status': 'error',
                                'message': 'Court not found'
                            })
                        booking.court_id = court_id
                    except Exception as e:
                        log.error(f"Error checking court existence: {str(e)}")
                        try:
                            self.request.tm.abort()
                        except Exception as abort_error:
                            log.error(f"Error aborting transaction: {str(abort_error)}")
                        return HTTPBadRequest(json={
                            'status': 'error',
                            'message': f'Error checking court: {str(e)}'
                        })
                
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
                
                try:
                    self.request.dbsession.flush()
                    
                    return {
                        'status': 'success',
                        'message': 'Booking updated successfully',
                        'booking': self._booking_to_dict(booking)
                    }
                except Exception as e:
                    log.error(f"Error flushing booking update: {str(e)}")
                    try:
                        self.request.tm.abort()
                    except Exception as abort_error:
                        log.error(f"Error aborting transaction: {str(abort_error)}")
                    return HTTPBadRequest(json={
                        'status': 'error',
                        'message': f'Error updating booking: {str(e)}'
                    })
            except ValidationError as e:
                # Tangani error validasi dari Marshmallow
                try:
                    self.request.tm.abort()
                except Exception as abort_error:
                    log.error(f"Error aborting transaction: {str(abort_error)}")
                return HTTPUnprocessableEntity(json={
                    'status': 'error',
                    'message': 'Validation error',
                    'errors': e.messages
                })
            except IntegrityError as e:
                log.error(f"Integrity error: {str(e)}")
                try:
                    self.request.tm.abort()
                except Exception as abort_error:
                    log.error(f"Error aborting transaction: {str(abort_error)}")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': 'Update would violate unique constraints'
                })
            except Exception as e:
                log.error(f"Database error when updating booking: {str(e)}")
                try:
                    self.request.tm.abort()
                except Exception as abort_error:
                    log.error(f"Error aborting transaction: {str(abort_error)}")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': str(e)
                })
        except ValueError as e:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Invalid booking ID: {str(e)}'
            })
        except Exception as e:
            log.error(f"Unexpected error in booking update: {str(e)}")
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            })

    @view_config(request_method='DELETE', renderer='json')
    def delete(self):
        try:
            booking_id = int(self.request.matchdict['id'])
            try:
                booking = self.request.dbsession.query(BookingORM).filter(BookingORM.id == booking_id).first()
                
                if booking is None:
                    return HTTPNotFound(json={
                        'status': 'error',
                        'message': 'Booking not found'
                    })
                
                try:
                    self.request.dbsession.delete(booking)
                    return {
                        'status': 'success',
                        'message': 'Booking deleted successfully',
                        'id': booking_id
                    }
                except Exception as e:
                    log.error(f"Error deleting booking: {str(e)}")
                    try:
                        self.request.tm.abort()
                    except Exception as abort_error:
                        log.error(f"Error aborting transaction: {str(abort_error)}")
                    return HTTPBadRequest(json={
                        'status': 'error',
                        'message': f'Error deleting booking: {str(e)}'
                    })
            except Exception as e:
                log.error(f"Database error when fetching booking for deletion: {str(e)}")
                try:
                    self.request.tm.abort()
                except Exception as abort_error:
                    log.error(f"Error aborting transaction: {str(abort_error)}")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': f'Error fetching booking for deletion: {str(e)}'
                })
        except ValueError as e:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Invalid booking ID: {str(e)}'
            })
        except Exception as e:
            log.error(f"Unexpected error in booking deletion: {str(e)}")
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            })
    
    def _booking_to_dict(self, booking):
        try:
            # Get court name for the booking
            court_name = "Unknown Court"
            try:
                court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == booking.court_id).first()
                if court:
                    court_name = court.court_name
            except Exception as e:
                log.error(f"Error fetching court data for booking {booking.id}: {str(e)}")
            
            # Get user information
            user_email = "Unknown User"
            try:
                user = self.request.dbsession.query(UserORM).filter(UserORM.id == booking.user_id).first()
                if user:
                    user_email = user.email
            except Exception as e:
                log.error(f"Error fetching user data for booking {booking.id}: {str(e)}")
            
            return {
                'id': booking.id,
                'user_id': booking.user_id,
                'user_email': user_email,
                'court_id': booking.court_id,
                'court_name': court_name,
                'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
                'time_slot': booking.time_slot,
                'full_name': booking.full_name,
                'phone_number': booking.phone_number,
                'status': booking.status
            }
        except Exception as e:
            log.error(f"Error in _booking_to_dict: {str(e)}")
            # Return minimal booking data to avoid breaking the API response
            return {
                'id': getattr(booking, 'id', 'unknown'),
                'status': getattr(booking, 'status', 'unknown'),
                'error': 'Error processing booking data'
            }

@view_defaults(route_name='admin_booking_status', permission='admin')
class AdminBookingStatusViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='PUT', renderer='json')
    def update_status(self):
        try:
            booking_id = int(self.request.matchdict['id'])
            try:
                booking = self.request.dbsession.query(BookingORM).filter(BookingORM.id == booking_id).first()
                
                if booking is None:
                    return HTTPNotFound(json={
                        'status': 'error',
                        'message': 'Booking not found'
                    })
                
                # Validasi status
                if 'status' not in self.request.json_body:
                    return HTTPBadRequest(json={
                        'status': 'error',
                        'message': 'Status field is required'
                    })
                    
                new_status = self.request.json_body['status']
                valid_statuses = ['pending', 'confirmed', 'cancelled']
                
                if new_status not in valid_statuses:
                    return HTTPBadRequest(json={
                        'status': 'error',
                        'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                    })
                    
                # Update status
                booking.status = new_status
                try:
                    self.request.dbsession.flush()
                    
                    log.info(f"Admin updated booking {booking_id} status to {new_status}")
                    
                    return {
                        'status': 'success',
                        'message': 'Booking status updated successfully',
                        'booking': self._booking_to_dict(booking)
                    }
                except Exception as e:
                    log.error(f"Error flushing booking status update: {str(e)}")
                    try:
                        self.request.tm.abort()
                    except Exception as abort_error:
                        log.error(f"Error aborting transaction: {str(abort_error)}")
                    return HTTPBadRequest(json={
                        'status': 'error',
                        'message': f'Error updating booking status: {str(e)}'
                    })
            except Exception as e:
                log.error(f"Database error when fetching booking for status update: {str(e)}")
                try:
                    self.request.tm.abort()
                except Exception as abort_error:
                    log.error(f"Error aborting transaction: {str(abort_error)}")
                return HTTPBadRequest(json={
                    'status': 'error',
                    'message': f'Error fetching booking for status update: {str(e)}'
                })
        except ValueError as e:
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Invalid booking ID: {str(e)}'
            })
        except Exception as e:
            log.error(f"Unexpected error in booking status update: {str(e)}")
            return HTTPBadRequest(json={
                'status': 'error',
                'message': f'Error updating booking status: {str(e)}'
            })
    
    def _booking_to_dict(self, booking):
        try:
            # Get court name for the booking
            court_name = "Unknown Court"
            try:
                court = self.request.dbsession.query(CourtORM).filter(CourtORM.id_court == booking.court_id).first()
                if court:
                    court_name = court.court_name
            except Exception as e:
                log.error(f"Error fetching court data for booking {booking.id}: {str(e)}")
            
            return {
                'id': booking.id,
                'user_id': booking.user_id,
                'court_id': booking.court_id,
                'court_name': court_name,
                'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
                'time_slot': booking.time_slot,
                'full_name': booking.full_name,
                'phone_number': booking.phone_number,
                'status': booking.status
            }
        except Exception as e:
            log.error(f"Error in _booking_to_dict: {str(e)}")
            # Return minimal booking data to avoid breaking the API response
            return {
                'id': getattr(booking, 'id', 'unknown'),
                'status': getattr(booking, 'status', 'unknown'),
                'error': 'Error processing booking data'
            }
