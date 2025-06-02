import React, { useEffect, useState } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

const PrivateRoute = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    // Check if user is authenticated
    const authToken = localStorage.getItem('authToken');
    setIsAuthenticated(!!authToken);
    setLoading(false);
  }, []);

  if (loading) {
    // You can add a loading spinner here if you want
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        <span className="ml-3">Loading...</span>
      </div>
    );
  }

  // If not authenticated, redirect to login page with the return url
  return isAuthenticated ? (
    <Outlet />
  ) : (
    <Navigate to="/login" state={{ from: location }} replace />
  );
};

export default PrivateRoute;
