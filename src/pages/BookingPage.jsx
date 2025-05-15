// src/pages/BookingPage.jsx
import React, { useState, useEffect } from "react";

function BookingPage() {
  const [availability, setAvailability] = useState([
    { id: 1, court: "Futsal - Lapangan 1", time: "09:00 - 10:00", status: "available" },
    { id: 2, court: "Basket - Lapangan 1", time: "10:00 - 11:00", status: "available" },
    { id: 3, court: "Futsal - Lapangan 2", time: "11:00 - 12:00", status: "booked" },
    { id: 4, court: "Basket - Lapangan 2", time: "12:00 - 13:00", status: "available" },
  ]);

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-200">
      <h2 className="text-2xl font-semibold mt-4">Pilih Lapangan dan Waktu</h2>
      <div className="grid grid-cols-2 gap-4 mt-8">
        {availability.map((slot) => (
          <div
            key={slot.id}
            className={`p-4 rounded-lg cursor-pointer ${
              slot.status === "booked" ? "bg-red-300" : "bg-green-300"
            } hover:${slot.status === "available" ? "bg-green-500" : ""}`}
          >
            <h3>{slot.court}</h3>
            <p>{slot.time}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default BookingPage;
