// src/pages/HistoryPage.jsx
import React, { useState, useEffect } from "react";

function HistoryPage() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // Gantilah dengan pemanggilan API atau data yang relevan
    setHistory([
      { id: 1, court: "Futsal - Lapangan 1", date: "2025-05-14", time: "09:00 - 10:00" },
      { id: 2, court: "Basket - Lapangan 1", date: "2025-05-14", time: "10:00 - 11:00" },
    ]);
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-200">
      <h2 className="text-2xl font-semibold mt-4">Booking History</h2>
      <div className="mt-8 w-full max-w-3xl">
        <table className="min-w-full table-auto bg-white rounded-lg shadow-md">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Court</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Date</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Time</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr key={item.id} className="border-t">
                <td className="px-6 py-3 text-sm text-gray-700">{item.court}</td>
                <td className="px-6 py-3 text-sm text-gray-700">{item.date}</td>
                <td className="px-6 py-3 text-sm text-gray-700">{item.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default HistoryPage;
