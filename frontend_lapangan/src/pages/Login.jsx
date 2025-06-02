import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FaSpinner } from 'react-icons/fa';
import axios from 'axios';
import '../styles/Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:6543/login', {
        email,
        password
      });

      const { token, role, name } = response.data;

      // Store auth data
      localStorage.setItem('authToken', token);
      localStorage.setItem('userRole', role);
      localStorage.setItem('userName', name);

      // Redirect based on role
      if (role === 'admin') {
        navigate('/admin/dashboard');
      } else {
        navigate('/');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.message || 'Failed to login. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">Login</h1>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="email">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form-input"
              placeholder="Enter your email"
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
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-input"
              placeholder="Enter your password"
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
                <span>Logging in...</span>
              </>
            ) : (
              'Login'
            )}
          </button>
        </form>

        <div className="register-link">
          Don't have an account?{' '}
          <Link to="/register">Register here</Link>
        </div>
      </div>
    </div>
  );
}

export default Login; 