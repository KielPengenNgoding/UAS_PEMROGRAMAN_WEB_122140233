import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FaSpinner } from 'react-icons/fa';
import axios from 'axios';
import '../styles/Register.css';

function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone_number: '',
    password: '',
    confirm_password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    // Validate passwords match
    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post('http://localhost:6543/register', {
        name: formData.name,
        email: formData.email,
        phone_number: formData.phone_number,
        password: formData.password
      });

      setSuccess('Registration successful! Redirecting to login...');
      
      // Clear form
      setFormData({
        name: '',
        email: '',
        phone_number: '',
        password: '',
        confirm_password: ''
      });

      // Redirect to login after 2 seconds
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.response?.data?.message || 'Failed to register. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h1 className="register-title">Register</h1>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {success && (
          <div className="success-message">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">
              Full Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="form-input"
              placeholder="Enter your full name"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="form-input"
              placeholder="Enter your email"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="phone_number">
              Phone Number
            </label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              className="form-input"
              placeholder="Enter your phone number"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="form-input"
              placeholder="Enter your password"
              required
            />
            <p className="form-helper">
              Password must be at least 6 characters long
            </p>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="confirm_password">
              Confirm Password
            </label>
            <input
              type="password"
              id="confirm_password"
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              className="form-input"
              placeholder="Confirm your password"
              required
            />
          </div>

          <button
            type="submit"
            className="button button-primary"
            disabled={loading}
          >
            {loading ? (
              <>
                <FaSpinner className="loading-spinner" />
                <span>Registering...</span>
              </>
            ) : (
              'Register'
            )}
          </button>
        </form>

        <div className="login-link">
          Already have an account?{' '}
          <Link to="/login">Login here</Link>
        </div>
      </div>
    </div>
  );
}

export default Register; 