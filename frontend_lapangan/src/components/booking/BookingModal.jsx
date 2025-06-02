import React from 'react';
import { FaSpinner } from 'react-icons/fa';

const BookingModal = ({
  selectedCourt,
  bookingData,
  onInputChange,
  onSubmit,
  onClose,
  loading,
  error
}) => {
  // Get today's date in YYYY-MM-DD format for min date
  const today = new Date().toISOString().split('T')[0];
  
  // Get current hour
  const currentHour = new Date().getHours();
  
  // Generate available hours (8:00 - 22:00)
  const availableHours = Array.from({ length: 14 }, (_, i) => i + 8)
    .filter(hour => {
      // If booking for today, only show future hours
      if (bookingData.booking_date === today) {
        return hour > currentHour;
      }
      return true;
    });

  return (
    <div className="booking-modal">
      <div className="modal-content">
        <h3 className="modal-title">Book {selectedCourt.court_name}</h3>
        <p className="modal-description">
          Please fill in your details to book this court.
        </p>

        {error && (
          <div className="error-message mb-4">
            {error}
          </div>
        )}

        <form onSubmit={onSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="full_name">
              Full Name
            </label>
            <input
              type="text"
              id="full_name"
              name="full_name"
              value={bookingData.full_name}
              onChange={onInputChange}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="phone_number">
              Phone Number
            </label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={bookingData.phone_number}
              onChange={onInputChange}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="booking_date">
              Date
            </label>
            <input
              type="date"
              id="booking_date"
              name="booking_date"
              value={bookingData.booking_date}
              onChange={onInputChange}
              className="form-input"
              min={today}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="booking_time">
              Time Slot
            </label>
            <select
              id="booking_time"
              name="booking_time"
              value={bookingData.booking_time}
              onChange={onInputChange}
              className="form-select"
              required
              disabled={!bookingData.booking_date} // Disable if no date selected
            >
              <option value="">Select time slot</option>
              {availableHours.map((hour) => {
                const nextHour = hour + 1;
                return (
                  <option key={hour} value={`${hour.toString().padStart(2, '0')}:00`}>
                    {hour.toString().padStart(2, '0')}.00 - {nextHour.toString().padStart(2, '0')}.00
                  </option>
                );
              })}
            </select>
            <p className="form-helper">
              Operating hours: 8:00 - 22:00
            </p>
          </div>

          <div className="button-group">
            <button
              type="button"
              onClick={onClose}
              className="button button-secondary"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="button button-primary"
              disabled={loading}
            >
              {loading ? (
                <>
                  <FaSpinner className="loading-spinner mr-2" />
                  Booking...
                </>
              ) : (
                'Book Now'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default BookingModal; 