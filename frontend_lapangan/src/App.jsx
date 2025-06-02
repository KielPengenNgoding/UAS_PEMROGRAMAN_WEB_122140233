// 📁 File: src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import BookingPage from "./pages/BookingPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import Dashboard from "./pages/Dashboard";
import HistoryPage from "./pages/HistoryPage";
import PrivateRoute from "./components/PrivateRoute";
import AdminRoute from "./components/AdminRoute";

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Navbar />
        <main className="pt-16">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            
            {/* Admin Protected Routes */}
            <Route element={<AdminRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
            </Route>
            
            {/* User Protected Routes */}
            <Route element={<PrivateRoute />}>
              <Route path="/booking" element={<BookingPage />} />
              <Route path="/history" element={<HistoryPage />} />
            </Route>
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
