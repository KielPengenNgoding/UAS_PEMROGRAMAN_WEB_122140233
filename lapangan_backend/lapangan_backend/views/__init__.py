from .default import my_view as home
from .user import UserViews, UserDetailViews
from .court import CourtViews, CourtDetailViews
from .booking import BookingViews, BookingDetailViews, CourtBookingViews
from .admin_booking import AdminBookingViews, AdminBookingDetailViews, AdminBookingStatusViews
from .admin_court import AdminCourtViews, AdminCourtDetailViews, AdminCourtUploadViews

def includeme(config):
    config.scan('.user')
    config.scan('.court')
    config.scan('.booking')
    config.scan('.admin_booking')
    config.scan('.admin_court')

__all__ = [
    'home',
    'UserViews',
    'UserDetailViews',
    'CourtViews',
    'CourtDetailViews',
    'BookingViews',
    'BookingDetailViews',
    'CourtBookingViews',
    'AdminBookingViews',
    'AdminBookingDetailViews',
    'AdminBookingStatusViews',
    'AdminCourtViews',
    'AdminCourtDetailViews',
    'AdminCourtUploadViews'
]