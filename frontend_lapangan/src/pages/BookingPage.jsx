import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../styles/BookingPage.css';

// Import components
import CourtCard from '../components/booking/CourtCard';
import BookingModal from '../components/booking/BookingModal';

function BookingPage() {
  const [courts, setCourts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedCourt, setSelectedCourt] = useState(null);
  const [bookingData, setBookingData] = useState({
    full_name: '',
    phone_number: '',
    booking_date: '',
    booking_time: ''
  });
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingError, setBookingError] = useState('');
  const navigate = useNavigate();

  const fetchCourts = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:6543/courts');
      
      // Transform court data
      const transformedCourts = response.data.data.map(court => {
        // Log untuk debugging
        console.log('Court data from backend:', court);
        
        return {
          ...court,
          // Pastikan image_url selalu string atau null
          image_url: court.image_url || null,
          // Pastikan description memiliki nilai default
          description: court.description || `${court.court_category} Court`,
          // Pastikan status dalam lowercase
          status: (court.status || 'available').toLowerCase()
        };
      });
      
      console.log('Transformed courts:', transformedCourts);
      setCourts(transformedCourts);
      setLoading(false);
    } catch (error) {
      console.log('Error fetching courts:', error);
      
      // Extract the specific error message from the response if available
      let errorMessage = 'Failed to load courts. Please try again later.';
      
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        if (error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (typeof error.response.data === 'string' && error.response.data.includes('booking conflict')) {
          errorMessage = 'This court is already booked for the selected date and time slot.';
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setError(errorMessage);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourts();
  }, []);

  const handleCourtSelect = (court) => {
    if (court.status === 'available') {
      console.log('Selected court:', court);
      setSelectedCourt(court);
      setBookingError('');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBookingData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCloseModal = () => {
    setSelectedCourt(null);
    setBookingData({
      full_name: '',
      phone_number: '',
      booking_date: '',
      booking_time: ''
    });
    setBookingError('');
  };

  const handleSubmitBooking = async (e) => {
    e.preventDefault();
    setBookingLoading(true);
    setBookingError('');

    try {
      // Validasi tanggal dan waktu
      if (!bookingData.booking_date) {
        throw new Error("Please select a date");
      }
      if (!bookingData.booking_time) {
        throw new Error("Please select a time");
      }

      // Log data sebelum dikirim
      console.log('Booking data before submission:', {
        date: bookingData.booking_date,
        time: bookingData.booking_time,
        fullData: bookingData
      });
      
      // Format time slot based on selected time (assuming 1-hour slots)
      const selectedHour = bookingData.booking_time.split(':')[0];
      const nextHour = parseInt(selectedHour) + 1;
      const timeSlot = `${selectedHour}.00 - ${nextHour}.00`;
      
      // Validasi waktu booking
      const now = new Date();
      const bookingDate = new Date(bookingData.booking_date);
      if (bookingDate < now && bookingDate.toDateString() !== now.toDateString()) {
        throw new Error("Cannot book for past date");
      }

      const userId = localStorage.getItem('userId');
      const authToken = localStorage.getItem('authToken');

      if (!userId || !authToken) {
        navigate('/login');
        return;
      }

      // Log data yang akan dikirim ke server
      const requestData = {
        court_id: selectedCourt.id_court,
        user_id: parseInt(userId),
        full_name: bookingData.full_name,
        phone_number: bookingData.phone_number,
        booking_date: bookingData.booking_date,
        time_slot: timeSlot
      };
      console.log('Data to be sent to server:', requestData);
      
      const response = await axios.post(`http://localhost:6543/bookings/users/${userId}`, requestData, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.data) {
        alert('Booking successful!');
        handleCloseModal();
        fetchCourts(); // Refresh courts list
      }
    } catch (err) {
      console.error('Error creating booking:', err);
      if (err.message === "Please select a date" || err.message === "Please select a time" || err.message === "Cannot book for past date/time") {
        setBookingError(err.message);
      } else {
        setBookingError(err.response?.data?.detail?.validation_errors || err.response?.data?.detail || 'Failed to create booking. Please try again.');
      }
    } finally {
      setBookingLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="booking-container">
        <div className="flex justify-center items-center min-h-screen">
          <div className="text-center">
            <div className="loading-spinner text-4xl text-blue-500 mb-4" />
            <p>Loading courts...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="booking-container">
        <div className="flex justify-center items-center min-h-screen">
          <div className="text-center">
            <p className="text-red-500 mb-4">{error}</p>
            <button
              onClick={fetchCourts}
              className="button button-primary"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="booking-container">
      <h1 className="booking-title">Available Courts</h1>

      <div className="courts-grid">
        {courts.map((court) => (
          <CourtCard
            key={court.id_court}
            court={court}
            onClick={() => handleCourtSelect(court)}
            disabled={court.status !== 'available'}
          />
        ))}
      </div>

      {selectedCourt && (
        <BookingModal
          selectedCourt={selectedCourt}
          bookingData={bookingData}
          onInputChange={handleInputChange}
          onSubmit={handleSubmitBooking}
          onClose={handleCloseModal}
          loading={bookingLoading}
          error={bookingError}
        />
      )}
    </div>
  );
}

export default BookingPage;
