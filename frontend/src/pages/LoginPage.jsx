import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Mock authentication
      if (email === 'user@example.com' && password === 'password123') {
        navigate('/home'); // Redirect to home page
      } else {
        setError('Invalid email or password');
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-wrapper">
        <div className="brand-section">
          <div className="logo-container">
            <span className="logo-icon">SR</span>
          </div>
          <h1 className="brand-name">StudyRight</h1>
          <p className="brand-tagline">Transform your lecture materials into engaging short-form videos</p>
          
          <div className="features-list">
            <div className="feature-item">
              <span className="feature-icon">📚</span>
              <span className="feature-text">Upload any document</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">🎬</span>
              <span className="feature-text">Generate video content</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">📱</span>
              <span className="feature-text">Learn on any device</span>
            </div>
          </div>
        </div>
        
        <div className="form-section">
          <div className="form-container">
            <h2>Welcome Back</h2>
            <p className="form-subtitle">Sign in to continue learning</p>
            
            {error && <div className="error-message">{error}</div>}
            
            <form onSubmit={handleLogin}>
              <div className="input-group">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your.email@example.com"
                  required
                />
              </div>
              
              <div className="input-group">
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="•••••••••••"
                  required
                />
              </div>
              
              <div className="forgot-password">
                <a href="#">Forgot password?</a>
              </div>
              
              <button 
                type="submit" 
                className={`login-button ${isLoading ? 'loading' : ''}`}
                disabled={isLoading}
              >
                {isLoading ? 'Signing in...' : 'Sign In'}
              </button>
            </form>
            
            <div className="register-prompt">
              <span>Don't have an account?</span>
              <a href="#" className="register-link">Create account</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;