import React, { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { FaUserCircle, FaSignOutAlt } from "react-icons/fa";

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState("");
  const [userName, setUserName] = useState("");
  
  useEffect(() => {
    // Check authentication status on every route change
    const authToken = localStorage.getItem("authToken");
    const storedUserRole = localStorage.getItem("userRole");
    const storedUserName = localStorage.getItem("userName");
    
    setIsLoggedIn(!!authToken);
    setUserRole(storedUserRole || "");
    setUserName(storedUserName || "");
  }, [location]);
  
  const isAdmin = userRole === "admin";

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    localStorage.removeItem("userRole");
    localStorage.removeItem("userName");
    localStorage.removeItem("userId");
    
    setIsLoggedIn(false);
    setUserRole("");
    setUserName("");
    
    navigate("/login");
  };

  return (
    <nav className="fixed top-0 left-0 right-0 bg-blue-600 text-white shadow-md z-50">
      <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-xl font-bold text-white flex items-center">
          <span className="mr-2">⚽</span>
          <span>Sontang Field</span>
        </Link>
        
        <div className="flex gap-6 items-center">
          <Link to="/" className="hover:text-blue-200 transition-colors">Home</Link>
          
          {isLoggedIn && (
            <Link to="/booking" className="hover:text-blue-200 transition-colors">Booking</Link>
          )}

          {!isLoggedIn && (
            <>
              <Link to="/login" className="hover:text-blue-200 transition-colors">Login</Link>
              <Link to="/register" className="bg-white text-blue-600 px-3 py-1 rounded-md hover:bg-blue-100 transition-colors">Register</Link>
            </>
          )}

          {isLoggedIn && isAdmin && (
            <Link to="/dashboard" className="hover:text-blue-200 transition-colors">Dashboard</Link>
          )}

          {isLoggedIn && (
            <>
              <Link to="/history" className="hover:text-blue-200 transition-colors">History</Link>
              
              <div className="flex items-center ml-4">
                <div className="flex items-center mr-4">
                  <FaUserCircle className="text-xl mr-2" />
                  <span className="text-sm">{userName}</span>
                </div>
                
                <button 
                  onClick={handleLogout} 
                  className="flex items-center text-sm bg-red-500 hover:bg-red-600 px-3 py-1 rounded transition-colors"
                >
                  <FaSignOutAlt className="mr-1" />
                  <span>Logout</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
