import React, { useEffect, useState } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

const AdminRoute = () => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    // Check if user is authenticated and has admin role
    const authToken = localStorage.getItem('authToken');
    const userRole = localStorage.getItem('userRole');
    
    setIsAdmin(!!authToken && userRole === 'admin');
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        <span className="ml-3">Loading...</span>
      </div>
    );
  }

  // If not admin, redirect to login page or history page
  return isAdmin ? (
    <Outlet />
  ) : (
    <Navigate to="/login" state={{ from: location }} replace />
  );
};

export default AdminRoute;
