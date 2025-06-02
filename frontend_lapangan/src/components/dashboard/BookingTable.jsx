import React from 'react';
import { FaSpinner } from 'react-icons/fa';

const BookingTable = ({ bookings, loading, onUpdateStatus, editBookingId }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case "confirmed":
        return "bg-green-100 text-green-800";
      case "pending":
        return "bg-yellow-100 text-yellow-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      case "completed":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-10">
        <FaSpinner className="animate-spin text-blue-500 text-3xl" />
        <span className="ml-3">Loading data...</span>
      </div>
    );
  }

  if (bookings.length === 0) {
    return (
      <div className="text-center py-10 text-gray-500">
        <p>Belum ada booking.</p>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className="data-table">
        <thead className="table-header">
          <tr>
            <th>User</th>
            <th>Phone</th>
            <th>Date</th>
            <th>Time</th>
            <th>Court</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {bookings.map((booking) => (
            <tr key={booking.id} className="table-row">
              <td className="table-cell">{booking.user}</td>
              <td className="table-cell">{booking.phone}</td>
              <td className="table-cell">{booking.date}</td>
              <td className="table-cell">{booking.time}</td>
              <td className="table-cell">{booking.court}</td>
              <td className="table-cell">
                <span className={`status-badge ${getStatusColor(booking.status)}`}>
                  {booking.status}
                </span>
                
                <div className="mt-2">
                  <select
                    className="text-xs border rounded p-1 bg-white"
                    value=""
                    onChange={(e) => {
                      if (e.target.value) {
                        onUpdateStatus(booking.id, e.target.value);
                        e.target.value = "";
                      }
                    }}
                    disabled={editBookingId === booking.id}
                  >
                    <option value="">Ubah status...</option>
                    <option value="pending">Pending</option>
                    <option value="confirmed">Confirmed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                  {editBookingId === booking.id && (
                    <span className="ml-2 text-xs text-blue-500">
                      <FaSpinner className="inline animate-spin" /> Updating...
                    </span>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BookingTable; 