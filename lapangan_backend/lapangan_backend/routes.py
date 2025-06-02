def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    # Home route
    config.add_route('home', '/')
    
    # User routes
    config.add_route('user', '/users')
    config.add_route('user_detail', '/users/{id}')
    
    # Court routes
    config.add_route('court', '/courts')
    config.add_route('court_detail', '/courts/{id_court}')
    
    # Booking routes
    config.add_route('booking', '/bookings/users/{user_id}')
    config.add_route('booking_detail', '/bookings/{id}/users/{user_id}')
    config.add_route('court_booking', '/bookings/courts/{court_id}')
    config.add_route('all_bookings', '/bookings')
    
    # Admin routes
    config.add_route('admin_bookings', '/admin/bookings')
    config.add_route('admin_booking_detail', '/admin/bookings/{id}')
    config.add_route('admin_booking_status', '/admin/bookings/{id}/status')
    
    # Admin court routes
    config.add_route('admin_courts', '/admin/courts')
    config.add_route('admin_court_detail', '/admin/courts/{id_court}')
    config.add_route('admin_court_upload_image', '/admin/courts/{id_court}/upload-image')
