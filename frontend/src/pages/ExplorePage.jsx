import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ExplorePage.css';
import VideoReels from "../components/VideoReels";

const ExplorePage = () => {
  const navigate = useNavigate();
  
  return (
    <div className="explore-page">
      <header className="app-header">
        <div className="logo" onClick={() => navigate('/')}>
          <span className="logo-icon">SR</span>
          <span className="logo-text">StudyRight</span>
        </div>
        <nav className="nav-menu">
          <button className="nav-button" onClick={() => navigate('/')}>Home</button>
          <button className="nav-button active" onClick={() => navigate('/explore')}>Explore</button>
          <button className="nav-button logout" onClick={() => navigate('/login')}>Logout</button>
        </nav>
      </header>

      <main className="explore-content">
        <VideoReels />
      </main>
    </div>
  );
};

export default ExplorePage;