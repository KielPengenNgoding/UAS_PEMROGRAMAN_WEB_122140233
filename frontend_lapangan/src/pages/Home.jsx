import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center px-6">
      <div className="max-w-4xl w-full text-center animate-fade-in">
        <h1 className="text-4xl sm:text-5xl font-bold mb-4">
          Welcome to <span className="text-yellow-300">Sontang Field</span>
        </h1>
        <p className="text-lg sm:text-xl text-white/80 mb-8">
          Your favorite place to play futsal and basketball!
        </p>
        <button
          onClick={() => navigate("/booking")}
          className="bg-yellow-400 text-black font-semibold px-6 py-3 rounded-full shadow-md hover:scale-105 hover:shadow-lg transition-transform duration-300"
        >
          Book Your Slot Now!
        </button>
      </div>

      <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 text-white/60 text-sm">
        &copy; {new Date().getFullYear()} Sontang Field. All rights reserved.
      </div>
    </div>
  );
}

export default Home;