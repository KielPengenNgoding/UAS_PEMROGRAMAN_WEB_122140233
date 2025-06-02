import React from 'react';
import { FaEdit, FaTimes } from 'react-icons/fa';

const CourtTable = ({ courts, onEdit, onDelete }) => {
  if (courts.length === 0) {
    return (
      <p className="text-gray-500 text-center py-4">Belum ada lapangan yang tersedia.</p>
    );
  }

  return (
    <div className="table-container">
      <table className="data-table">
        <thead className="table-header">
          <tr>
            <th className="py-3 px-6 text-left">Nama Lapangan</th>
            <th className="py-3 px-6 text-left">Kategori</th>
            <th className="py-3 px-6 text-left">Status</th>
            <th className="py-3 px-6 text-left">Gambar</th>
            <th className="py-3 px-6 text-center">Aksi</th>
          </tr>
        </thead>
        <tbody className="text-gray-600 text-sm">
          {courts.map(court => (
            <tr key={court.id_court} className="table-row">
              <td className="table-cell">{court.court_name}</td>
              <td className="table-cell">{court.court_category}</td>
              <td className="table-cell">
                <span className={`status-badge ${
                  court.status === 'available' ? 'status-available' :
                  court.status === 'maintenance' ? 'status-maintenance' :
                  'status-booked'
                }`}>
                  {court.status === 'available' ? 'Available' :
                   court.status === 'maintenance' ? 'Maintenance' :
                   'Booked'}
                </span>
              </td>
              <td className="table-cell">
                {court.image_url ? (
                  <img 
                    src={`http://localhost:6543${court.image_url}`} 
                    alt={court.court_name} 
                    className="h-10 w-10 object-cover rounded"
                  />
                ) : (
                  <span className="text-gray-400">Tidak ada gambar</span>
                )}
              </td>
              <td className="table-cell text-center">
                <div className="flex item-center justify-center">
                  <button 
                    onClick={() => onEdit(court)}
                    className="transform hover:text-blue-500 hover:scale-110 transition-all duration-150 mr-3"
                  >
                    <FaEdit />
                  </button>
                  <button 
                    onClick={() => onDelete(court)}
                    className="transform hover:text-red-500 hover:scale-110 transition-all duration-150"
                  >
                    <FaTimes />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CourtTable; 