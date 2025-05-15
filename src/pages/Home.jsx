import React from "react";
import { Link } from "react-router-dom"; // Menggunakan Link dari react-router-dom

function Home() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
      <div className="text-center px-6 md:px-12 w-full max-w-screen-xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-extrabold leading-tight mb-4 animate__animated animate__fadeIn">
          Welcome to <span className="text-yellow-400">Sontang Field</span>
        </h1>
        <p className="text-xl md:text-2xl mb-6 animate__animated animate__fadeIn animate__delay-1s">
          Your favorite place to play futsal and basketball!
        </p>
        <img
          src="/assets/background.jpg"
          alt="Background"
          className="w-full md:w-3/4 lg:w-2/3 xl:w-1/2 rounded-lg shadow-xl transform transition-all hover:scale-105"
        />
        <div className="mt-8">
          {/* Menggunakan Link dari react-router-dom untuk navigasi tanpa refresh halaman */}
          <Link
            to="/booking"
            className="px-8 py-3 bg-yellow-400 text-black font-semibold rounded-full shadow-lg hover:bg-yellow-500 transition duration-300"
          >
            Book Your Slot Now!
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
