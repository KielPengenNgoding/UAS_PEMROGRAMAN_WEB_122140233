import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-blue-500 p-4">
      <ul className="flex justify-between">
        <li>
          <Link to="/" className="text-white font-bold">Sontang Field</Link>
        </li>
        <li>
          <Link to="/booking" className="text-white">Booking</Link>
        </li>
        <li>
          <Link to="/login" className="text-white">Login</Link>
        </li>
        <li>
          <Link to="/admin" className="text-white">Admin</Link>
        </li>
        <li>
          <Link to="/history" className="text-white">History</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
