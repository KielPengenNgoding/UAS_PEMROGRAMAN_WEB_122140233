import React, { useState } from "react";
import { FaUserCircle, FaChartLine, FaBook, FaHistory } from "react-icons/fa";

function Dashboard() {
  // Dummy data for table
  const orders = [
    { id: 1, user: "John Doe", date: "2025-05-14", time: "09:00 - 10:00", court: "Futsal 1", status: "Active" },
    { id: 2, user: "Jane Smith", date: "2025-05-14", time: "10:00 - 11:00", court: "Basket 1", status: "Completed" },
    { id: 3, user: "Mark Lee", date: "2025-05-14", time: "11:00 - 12:00", court: "Futsal 2", status: "Cancelled" },
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-700">Admin Dashboard</h2>
        <div className="flex items-center space-x-4">
          <FaUserCircle className="text-4xl text-blue-600 cursor-pointer" />
          <span className="text-lg font-medium text-gray-700">Admin</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mb-8">
        {/* Dashboard Statistics Cards */}
        <div className="bg-white p-6 rounded-lg shadow-md flex items-center space-x-4">
          <FaChartLine className="text-blue-500 text-3xl" />
          <div>
            <p className="text-gray-500">Total Bookings</p>
            <h3 className="text-2xl font-bold">125</h3>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md flex items-center space-x-4">
          <FaBook className="text-green-500 text-3xl" />
          <div>
            <p className="text-gray-500">Upcoming Bookings</p>
            <h3 className="text-2xl font-bold">25</h3>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md flex items-center space-x-4">
          <FaHistory className="text-orange-500 text-3xl" />
          <div>
            <p className="text-gray-500">Completed Bookings</p>
            <h3 className="text-2xl font-bold">100</h3>
          </div>
        </div>
      </div>

      {/* Orders Table */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-2xl font-bold mb-4 text-gray-700">Recent Orders</h3>
        <table className="min-w-full table-auto">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">User</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Date</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Time</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Court</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-600">Status</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id} className="border-t">
                <td className="px-6 py-3 text-sm text-gray-700">{order.user}</td>
                <td className="px-6 py-3 text-sm text-gray-700">{order.date}</td>
                <td className="px-6 py-3 text-sm text-gray-700">{order.time}</td>
                <td className="px-6 py-3 text-sm text-gray-700">{order.court}</td>
                <td className="px-6 py-3 text-sm text-gray-700">
                  <span
                    className={`px-3 py-1 rounded-full text-sm ${
                      order.status === "Active"
                        ? "bg-green-500 text-white"
                        : order.status === "Completed"
                        ? "bg-blue-500 text-white"
                        : "bg-red-500 text-white"
                    }`}
                  >
                    {order.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
