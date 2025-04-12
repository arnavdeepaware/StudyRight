import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const themes = [
  {
    background: "#1A1A2E",
    color: "#FFFFFF",
    primaryColor: "#0F3460",
  },
  {
    background: "#461220",
    color: "#FFFFFF",
    primaryColor: "#E94560",
  },
  {
    background: "#192A51",
    color: "#FFFFFF",
    primaryColor: "#967AA1",
  },
  {
    background: "#F7B267",
    color: "#000000",
    primaryColor: "#F4845F",
  },
  {
    background: "#F25F5C",
    color: "#000000",
    primaryColor: "#642B36",
  },
  {
    background: "#231F20",
    color: "#FFF",
    primaryColor: "#BB4430",
  },
];

const setTheme = (theme) => {
  const root = document.querySelector(":root");
  root.style.setProperty("--background", theme.background);
  root.style.setProperty("--color", theme.color);
  root.style.setProperty("--primary-color", theme.primaryColor);
};

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

  useEffect(() => {
    const btnContainer = document.querySelector(".theme-btn-container");
    themes.forEach((theme) => {
      const div = document.createElement("div");
      div.className = "theme-btn";
      div.style.cssText = `background: ${theme.background}; width: 25px; height: 25px; border-radius: 50%; margin: 5px; cursor: pointer;`;
      btnContainer.appendChild(div);
      div.addEventListener("click", () => setTheme(theme));
    });
  }, []);

  return (
    <div className="container">
      <div className="login-container">
        <div className="circle circle-one"></div>
        <div className="form-container">
          <img
            src="https://raw.githubusercontent.com/hicodersofficial/glassmorphism-login-form/master/assets/illustration.png"
            alt="illustration"
            className="illustration"
          />
          <h1 className="opacity">LOGIN</h1>
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
        <div className="circle circle-two"></div>
        <div className="theme-btn-container"></div>
      </div>
    </div>
  );
};

export default LoginPage;