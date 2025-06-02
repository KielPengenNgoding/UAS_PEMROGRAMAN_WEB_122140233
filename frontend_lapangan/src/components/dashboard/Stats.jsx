import React from 'react';
import { FaChartLine, FaBook, FaHistory, FaSpinner } from 'react-icons/fa';

const Stats = ({ loading, stats }) => {
  return (
    <div className="stats-grid">
      <div className="stats-card">
        <FaChartLine className="text-blue-500 text-3xl" />
        <div>
          <p className="text-gray-500">Total Bookings</p>
          <h3 className="text-2xl font-bold">
            {loading ? <FaSpinner className="animate-spin" /> : stats.totalBookings}
          </h3>
        </div>
      </div>

      <div className="stats-card">
        <FaBook className="text-green-500 text-3xl" />
        <div>
          <p className="text-gray-500">Upcoming Bookings</p>
          <h3 className="text-2xl font-bold">
            {loading ? <FaSpinner className="animate-spin" /> : stats.upcomingBookings}
          </h3>
        </div>
      </div>

      <div className="stats-card">
        <FaHistory className="text-orange-500 text-3xl" />
        <div>
          <p className="text-gray-500">Completed Bookings</p>
          <h3 className="text-2xl font-bold">
            {loading ? <FaSpinner className="animate-spin" /> : stats.completedBookings}
          </h3>
        </div>
      </div>
    </div>
  );
};

export default Stats; 