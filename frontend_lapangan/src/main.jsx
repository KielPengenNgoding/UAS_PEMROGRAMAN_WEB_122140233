import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css"; // gunakan jika Anda punya file CSS global, bisa dihapus jika tidak ada

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
