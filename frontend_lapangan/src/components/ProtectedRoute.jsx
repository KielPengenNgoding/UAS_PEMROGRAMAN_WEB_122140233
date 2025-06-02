// 📁 File: src/components/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ role, children }) {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  const userRole = localStorage.getItem("userRole");

  if (!isLoggedIn) return <Navigate to="/login" />;
  if (role && userRole !== role) return <Navigate to="/" />;

  return children;
}

export default ProtectedRoute;
