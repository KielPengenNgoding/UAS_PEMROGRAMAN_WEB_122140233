// 📁 File: src/pages/RegisterPage.jsx
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const navigate = useNavigate();

  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    
    // Validasi password (harus mengandung minimal satu huruf kapital)
    if (!/[A-Z]/.test(password)) {
      setError("Password harus mengandung minimal satu huruf kapital");
      return;
    }
    
    try {
      const response = await axios.post("http://localhost:6543/auth/register", {
        full_name: name,
        email,
        password,
        role
      });
      
      alert("Registrasi berhasil! Silakan login.");
      navigate("/login");
    } catch (error) {
      console.error("Register error:", error);
      if (error.response && error.response.data && error.response.data.validation_errors) {
        // Menampilkan error validasi dari server
        const validationErrors = error.response.data.validation_errors;
        const errorMessages = Object.values(validationErrors).flat().join(', ');
        setError(errorMessages);
      } else if (error.response && error.response.status === 409) {
        setError("Email sudah terdaftar. Silakan gunakan email lain.");
      } else {
        setError("Terjadi kesalahan. Silakan coba lagi.");
      }
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-4 text-center">Register</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Nama lengkap" value={name}
            onChange={(e) => setName(e.target.value)}
            className="mb-3 w-full px-4 py-2 border border-gray-300 rounded-lg" required />
          <input type="email" placeholder="Email" value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mb-3 w-full px-4 py-2 border border-gray-300 rounded-lg" required />
          <input type="password" placeholder="Password" value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mb-3 w-full px-4 py-2 border border-gray-300 rounded-lg" required />
          <select value={role} onChange={(e) => setRole(e.target.value)}
            className="mb-4 w-full px-4 py-2 border border-gray-300 rounded-lg">
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
          <button type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600">
            Register
          </button>
        </form>
      </div>
    </div>
  );
}

export default RegisterPage;
