import React, { useState } from 'react';
import { config } from '../../config';
import { FaImage } from 'react-icons/fa';

const CourtCard = ({ court, onClick, disabled }) => {
  const [imageError, setImageError] = useState(false);

  const getStatusClass = (status) => {
    switch (status) {
      case "available":
        return "status-available";
      case "maintenance":
        return "status-maintenance";
      case "booked":
        return "status-booked";
      default:
        return "";
    }
  };

  const getDefaultImage = (category) => {
    const categoryLower = category.toLowerCase();
    
    if (categoryLower.includes('futsal')) {
      return `${config.baseUrl}/images/futsal1.jpg`;
    } else if (categoryLower.includes('basket')) {
      return `${config.baseUrl}/images/basket1.jpg`;
    } else if (categoryLower.includes('tennis')) {
      return `${config.baseUrl}/images/basket1.jpg`;  // Sementara menggunakan gambar basket
    } else if (categoryLower.includes('badminton')) {
      return `${config.baseUrl}/images/basket1.jpg`;  // Sementara menggunakan gambar basket
    } else if (categoryLower.includes('volley')) {
      return `${config.baseUrl}/images/basket1.jpg`;  // Sementara menggunakan gambar basket
    }
    return `${config.baseUrl}/images/basket1.jpg`;
  };

  // Handle image URL
  const getImageUrl = () => {
    if (imageError) {
      return null;
    }

    try {
      // If no image_url is provided, use default image based on category
      if (!court.image_url) {
        console.log('No image URL provided, using default for category:', court.court_category);
        return getDefaultImage(court.court_category);
      }
      
      // If the URL starts with /static/, prepend the backend URL
      if (court.image_url.startsWith('/static/')) {
        const fullUrl = `${config.backendUrl}${court.image_url}`;
        console.log('Using static URL:', fullUrl);
        return fullUrl;
      }
      // If the URL already starts with http, use it as is
      else if (court.image_url.startsWith('http')) {
        console.log('Using absolute URL:', court.image_url);
        return court.image_url;
      }
      // Otherwise, assume it's a relative path and prepend the images path
      else {
        const fullUrl = `${config.baseUrl}/images/${court.image_url}`;
        console.log('Using relative URL:', fullUrl);
        return fullUrl;
      }
    } catch (error) {
      console.error('Error processing image URL:', error);
      return getDefaultImage(court.court_category);
    }
  };

  return (
    <div 
      className={`court-card ${disabled ? 'disabled' : ''}`}
      onClick={disabled ? null : onClick}
    >
      <div className="court-image-container">
        {getImageUrl() ? (
          <img 
            src={getImageUrl()}
            alt={court.court_name}
            className="court-image"
            onError={(e) => {
              console.error('Image failed to load:', e.target.src);
              setImageError(true);
            }}
          />
        ) : (
          <div className="no-image-placeholder">
            <FaImage className="text-gray-400 w-12 h-12" />
            <p className="text-gray-500 text-sm mt-2">Tidak ada gambar</p>
          </div>
        )}
      </div>
      <div className="court-info">
        <h3 className="court-name">{court.court_name}</h3>
        <p className="court-description">{court.description || `${court.court_category} Court`}</p>
        <span className={`court-status ${getStatusClass(court.status)}`}>
          {court.status.charAt(0).toUpperCase() + court.status.slice(1)}
        </span>
      </div>
    </div>
  );
};

export default CourtCard; 