import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    // Mock authentication
    if (email === 'user@example.com' && password === 'password123') {
      alert('Login successful!');
      navigate('/home'); // Redirect to home page
    } else {
      alert('Invalid email or password.');
    }
  };

  return (
    <div className="container">
      <div className="main-container">
        {/* Left side - Brand section */}
        <div className="brand-container">
          <h1 className="brand-title">StudyRight</h1>
          <p id="colr" className="brand-tagline" style={{textAlign: 'center'}}>Welcome to your way of Studying Right</p>
        </div>
        
        {/* Right side - Login form */}
        <div className="login-container">
          <div className="form-container">
            <h1 className="opacity" style={{textAlign: 'center'}}>Sign In</h1>

            <form onSubmit={handleLogin}>
              <input
                type="email"
                placeholder="USERNAME"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="PASSWORD"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button type="submit" className="opacity">SUBMIT</button>
            </form>

            <div className="register-forget opacity">
              <a href="#">REGISTER</a>
              <a href="#">FORGOT PASSWORD</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;