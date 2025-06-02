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
