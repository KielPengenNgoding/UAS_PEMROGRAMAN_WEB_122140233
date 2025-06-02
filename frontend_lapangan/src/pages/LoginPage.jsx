// 📁 File: src/pages/LoginPage.jsx
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      console.log("Attempting login with:", { email, password: "[REDACTED]" });
      
      const response = await axios.post("http://localhost:6543/auth/login", {
        email,
        password
      });
      
      console.log("Login response:", {
        headers: response.headers,
        data: response.data
      });
      
      // Mendapatkan token dari header response
      // Cek berbagai kemungkinan nama header untuk token
      let authToken = response.headers.authorization;
      
      if (!authToken && response.headers['Authorization']) {
        authToken = response.headers['Authorization'];
      }
      
      // Cek jika token ada di response body (pendekatan baru)
      if (response.data && response.data.token) {
        authToken = response.data.token;
        console.log("Token ditemukan di response body!");
      }
      
      // Jika masih tidak ada token, coba cek di header dengan nama lain
      if (!authToken) {
        const headerKeys = Object.keys(response.headers).filter(key => 
          key.toLowerCase().includes('auth') || key.toLowerCase().includes('token'));
        
        if (headerKeys.length > 0) {
          authToken = response.headers[headerKeys[0]];
        }
      }
      
      console.log("Extracted auth token:", authToken ? "[TOKEN FOUND]" : "[NO TOKEN]");
      
      // Ekstrak role dari response
      let userRole = response.data.user && response.data.user.role ? response.data.user.role : null;
      
      // Jika tidak ada role di response.data.user, coba cari di tempat lain
      if (!userRole && response.data && response.data.role) {
        userRole = response.data.role;
      }
      
      console.log("Extracted user role:", userRole);
      
      // Jika tidak ada token atau role, tampilkan error
      if (!authToken) {
        setError("Tidak dapat menemukan token autentikasi. Silakan hubungi administrator.");
        return;
      }
      
      if (!userRole) {
        // Default ke user jika tidak ada role
        userRole = "user";
        console.log("No role found, defaulting to:", userRole);
      }
      
      // Menyimpan data user dan token ke localStorage
      localStorage.setItem("isLoggedIn", "true");
      localStorage.setItem("authToken", authToken);
      localStorage.setItem("userRole", userRole);
      localStorage.setItem("userName", response.data.user ? response.data.user.full_name : email);
      localStorage.setItem("userId", response.data.user ? response.data.user.id : "");
      
      console.log("Saved to localStorage:", {
        isLoggedIn: true,
        authToken: authToken ? "[TOKEN SAVED]" : "[NO TOKEN]",
        userRole,
        userName: response.data.user ? response.data.user.full_name : email,
        userId: response.data.user ? response.data.user.id : ""
      });
      
      // Redirect berdasarkan role
      if (userRole === "admin") {
        navigate("/dashboard");
      } else {
        navigate("/history");
      }
    } catch (error) {
      console.error("Login error:", error);
      console.log("Error response:", error.response ? error.response.data : "No response data");
      
      if (error.response && error.response.status === 401) {
        setError("Email atau password salah.");
      } else {
        setError("Terjadi kesalahan. Silakan coba lagi.");
      }
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleSubmit}>
          <input type="email" placeholder="Email" value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mb-3 w-full px-4 py-2 border border-gray-300 rounded-lg" required />
          <input type="password" placeholder="Password" value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mb-4 w-full px-4 py-2 border border-gray-300 rounded-lg" required />
          <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600">
            Login
          </button>
        </form>
        <p className="text-center text-sm mt-4">
          Belum punya akun? <Link to="/register" className="text-blue-600 hover:underline">Daftar di sini</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
