    def _booking_to_dict(self, booking):
        # Get court name if court relation is loaded
        court_name = None
        if hasattr(booking, 'court') and booking.court:
            court_name = booking.court.court_name
            
        return {
            'id': booking.id,
            'user_id': booking.user_id,
            'court_id': booking.court_id,
            'court_name': court_name,  # Include court name
            'booking_date': booking.booking_date.isoformat() if booking.booking_date else None,
            'time_slot': booking.time_slot,
            'full_name': booking.full_name,
            'phone_number': booking.phone_number,
            'status': booking.status
        }
