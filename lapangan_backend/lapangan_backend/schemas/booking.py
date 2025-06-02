from marshmallow import Schema, fields, validate, validates, ValidationError, post_load, validates_schema
from datetime import datetime, date, timedelta
import re
import logging
from .base import BaseSchema

log = logging.getLogger(__name__)

class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    court_id = fields.Int(required=True)
    booking_date = fields.Date(required=True)
    time_slot = fields.Str(required=True)
    full_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    status = fields.Str(
        validate=validate.OneOf(['pending', 'confirmed', 'cancelled']), 
        required=False
    )

    @validates_schema
    def validate_booking_time(self, data, **kwargs):
        """Validate booking date and time slot."""
        if 'booking_date' not in data:
            log.warning("booking_date missing from validation data")
            return
            
        if 'time_slot' not in data:
            log.warning("time_slot missing from validation data")
            return
            
        booking_date = data['booking_date']
        time_slot = data['time_slot']
        
        log.info(f"Validating booking_date: {booking_date}, type: {type(booking_date)}")
        log.info(f"Validating time_slot: {time_slot}, type: {type(time_slot)}")
        
        # Validate date is not in the past
        today = date.today()
        if booking_date < today:
            log.warning(f"Booking date {booking_date} is in the past (today: {today})")
            raise ValidationError("Booking date cannot be in the past", field_name="booking_date")
        
        # Validate time slot format (e.g., "08.00 - 09.00")
        time_slot_pattern = r'^([01]?[0-9]|2[0-3])\.00 - ([01]?[0-9]|2[0-3])\.00$'
        if not re.match(time_slot_pattern, time_slot):
            log.warning(f"Invalid time_slot format: {time_slot}")
            raise ValidationError("Time slot must be in format 'HH.00 - HH.00'", field_name="time_slot")
        
        try:
            # Extract start hour from time slot
            start_hour = int(time_slot.split(' - ')[0].split('.')[0])
            
            # Validate operating hours (8:00 - 22:00)
            if start_hour < 8 or start_hour >= 22:
                log.warning(f"Invalid booking hour: {start_hour}, must be between 8 and 21")
                raise ValidationError("Booking time must be between 08.00 and 22.00", field_name="time_slot")
        except (ValueError, IndexError) as e:
            log.error(f"Error parsing time_slot: {time_slot}, error: {str(e)}")
            raise ValidationError(f"Invalid time slot format: {str(e)}", field_name="time_slot")

    @post_load
    def set_defaults(self, data, **kwargs):
        """Set default values after validation."""
        if 'status' not in data or not data['status']:
            data['status'] = 'pending'
        return data

    def set_schema_by_method(self, method):
        """Adjust schema based on HTTP method."""
        if method == 'PUT':
            # For PUT requests, make all fields optional
            self.fields['user_id'].required = False
            self.fields['court_id'].required = False
            self.fields['booking_date'].required = False
            self.fields['time_slot'].required = False
            self.fields['full_name'].required = False
            self.fields['phone_number'].required = False
        elif method == 'POST':
            # For POST, all required fields remain required
            pass
