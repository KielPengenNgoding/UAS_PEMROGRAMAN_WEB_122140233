// src/pages/HistoryPage.jsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBookings = async () => {
      const userId = localStorage.getItem("userId");
      const authToken = localStorage.getItem("authToken");
      
      if (!userId || !authToken) {
        navigate("/login");
        return;
      }
      
      try {
        setLoading(true);
        // Gunakan withCredentials untuk mengirim cookie autentikasi
        const response = await axios.get(`http://localhost:6543/bookings/users/${userId}`, {
          withCredentials: true
        });
        
        console.log('Bookings response:', response.data);
        // Log each booking to see the exact structure
        if (response.data && response.data.data) {
          console.log('First booking example:', response.data.data[0]);
          console.log('Booking date type:', typeof response.data.data[0]?.booking_date);
          console.log('Time slot value:', response.data.data[0]?.time_slot);
        }
        
        // Get all unique court IDs from bookings
        const courtIds = [...new Set(response.data.data.map(booking => booking.court_id))];
        
        // Fetch court details for all court IDs
        const courtPromises = courtIds.map(async courtId => {
          try {
            const courtResponse = await axios.get(`http://localhost:6543/courts/${courtId}`, {
              withCredentials: true
            });
            return { id: courtId, name: courtResponse.data.court_name };
          } catch (err) {
            console.error(`Error fetching court ${courtId}:`, err);
            return { id: courtId, name: `Court ${courtId}` };
          }
        });
        
        // Wait for all court details to be fetched
        const courts = await Promise.all(courtPromises);
        const courtsMap = courts.reduce((map, court) => {
          map[court.id] = court.name;
          return map;
        }, {});
        
        console.log('Courts map:', courtsMap);
        
        // Format data booking untuk ditampilkan
        const formattedBookings = response.data.data.map(booking => {
          console.log('Processing booking:', booking);
          
          // Parse booking_date if it exists
          let formattedDate = 'Invalid Date';
          if (booking.booking_date) {
            const bookingDate = new Date(booking.booking_date);
            formattedDate = bookingDate.toLocaleDateString('id-ID', {
              year: 'numeric', 
              month: 'long', 
              day: 'numeric'
            });
          }
          
          // Use time_slot directly
          const formattedTime = booking.time_slot || 'Invalid Date';
          
          // Get court name from map or use court_name from booking if available
          const courtName = booking.court_name || courtsMap[booking.court_id] || `Court ${booking.court_id}`;
          
          return {
            id: booking.id,
            court: courtName,
            date: formattedDate,
            time: formattedTime,
            status: booking.status
          };
        });
        
        setHistory(formattedBookings);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching bookings:", err);
        setError("Gagal memuat data booking. Silakan coba lagi.");
        setLoading(false);
      }
    };
    
    fetchBookings();
  }, [navigate]);

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-200 p-4">
      <div className="w-full max-w-4xl bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-6 text-center">Booking History</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        
        {loading ? (
          <div className="flex justify-center items-center py-10">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            <span className="ml-3">Loading...</span>
          </div>
        ) : history.length === 0 ? (
          <div className="text-center py-10 text-gray-500">
            <p>Anda belum memiliki riwayat booking.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full table-auto">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Court</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Tanggal</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Waktu</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Status</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.id} className="border-t hover:bg-gray-50">
                    <td className="px-6 py-3 text-sm text-gray-700">{item.court}</td>
                    <td className="px-6 py-3 text-sm text-gray-700">{item.date}</td>
                    <td className="px-6 py-3 text-sm text-gray-700">{item.time}</td>
                    <td className="px-6 py-3 text-sm">
                      <span className={
                        `px-2 py-1 rounded-full text-xs font-semibold ${
                          item.status === 'confirmed' ? 'bg-green-100 text-green-800' : 
                          item.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                          item.status === 'cancelled' ? 'bg-red-100 text-red-800' : 
                          'bg-gray-100 text-gray-800'
                        }`
                      }>
                        {item.status === 'confirmed' ? 'Dikonfirmasi' : 
                         item.status === 'pending' ? 'Menunggu' : 
                         item.status === 'cancelled' ? 'Dibatalkan' : 
                         item.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default HistoryPage;
