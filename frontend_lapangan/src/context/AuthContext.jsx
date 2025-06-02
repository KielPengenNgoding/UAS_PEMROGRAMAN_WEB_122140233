// src/context/AuthContext.js
import React, { createContext, useState, useContext } from "react";

// Membuat context untuk autentikasi
const AuthContext = createContext();

// Provider untuk membungkus aplikasi dan memberikan state auth
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = (username, password) => {
    // Logika login (misalnya memeriksa username dan password)
    setUser({ username }); // Menyimpan info user saat login
  };

  const logout = () => {
    setUser(null); // Menghapus info user saat logout
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook untuk mengakses auth context di komponen lain
export const useAuth = () => {
  return useContext(AuthContext);
};
