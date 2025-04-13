import React, { useState } from 'react';
import './ExplorePage.css';
import { useNavigate } from 'react-router-dom';
import VideoGallery from "../components/VideoGallery";

const ExplorePage = () => {
  const [activePanel, setActivePanel] = useState(0);
  const navigate = useNavigate();

  // TODO: replace with actual userId from JWT or Mongo later
  const userId = 'replace_with_your_user_id_here';

  const panels = [
    {
      title: 'Machine Learning',
      color: '#4A90E2',
      description: 'Algorithms and statistical models that enable computers to learn'
    },
    {
      title: 'Data Structures',
      color: '#50C878',
      description: 'Efficient ways to organize and store data'
    },
    {
      title: 'Algorithms',
      color: '#9370DB',
      description: 'Step-by-step procedures for solving problems'
    },
    {
      title: 'Quantum Computing',
      color: '#FF6B6B',
      description: 'Computing using quantum-mechanical phenomena'
    },
    {
      title: 'Cybersecurity',
      color: '#FFD700',
      description: 'Protection of computer systems from theft and damage'
    },
  ];

  const handlePanelClick = (index) => {
    setActivePanel(index);
  };

  const handleBackClick = () => {
    navigate('/');
  };

  return (
    <div className="explore-container">
      <div className="header">
        <button 
          className="back-button" 
          onClick={handleBackClick}
          aria-label="Go back to home page"
        >
          <svg className="back-arrow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 12H5"></path>
            <path d="M12 19l-7-7 7-7"></path>
          </svg>
          <span>Back</span>
        </button>
        <h1 className="explore-title">Explore Topics</h1>
      </div>

      <div className="panels-container">
        {panels.map((panel, index) => (
          <div
            key={index}
            className={`panel ${index === activePanel ? 'active' : ''}`}
            style={{ 
              backgroundColor: panel.color,
              backgroundImage: `linear-gradient(to bottom, ${panel.color}80, ${panel.color})` 
            }}
            onClick={() => handlePanelClick(index)}
          >
            <div className="panel-content">
              <h3>{panel.title}</h3>
              <p className="panel-description">{panel.description}</p>
            </div>
            <div className="panel-icon">
              {getIconForTopic(panel.title)}
            </div>
          </div>
        ))}
      </div>

      {/* ✅ VideoGallery below the panels */}
      <div className="video-gallery-section">
        <h2 className="explore-subtitle">Your Generated Videos</h2>
        <VideoGallery userId={userId} />
      </div>
    </div>
  );
};

const getIconForTopic = (topic) => {
  switch(topic) {
    case 'Machine Learning':
      return '🧠';
    case 'Data Structures':
      return '🌲';
    case 'Algorithms':
      return '📊';
    case 'Quantum Computing':
      return '⚛️';
    case 'Cybersecurity':
      return '🔒';
    default:
      return '💻';
  }

  
};

export default ExplorePage;