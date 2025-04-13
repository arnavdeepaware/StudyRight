// ExplorePage.jsx
import React, { useState } from 'react';
import './ExplorePage.css';
import { useNavigate } from 'react-router-dom';

const ExplorePage = () => {
  const [activePanel, setActivePanel] = useState(0);
  const navigate = useNavigate();

  const panels = [
    {
      title: 'Machine Learning',
      color: '#4A90E2', // Blue
      description: 'Algorithms and statistical models that enable computers to learn'
    },
    {
      title: 'Data Structures',
      color: '#50C878', // Emerald
      description: 'Efficient ways to organize and store data'
    },
    {
      title: 'Algorithms',
      color: '#9370DB', // Medium Purple
      description: 'Step-by-step procedures for solving problems'
    },
    {
      title: 'Quantum Computing',
      color: '#FF6B6B', // Light Red
      description: 'Computing using quantum-mechanical phenomena'
    },
    {
      title: 'Cybersecurity',
      color: '#FFD700', // Gold
      description: 'Protection of computer systems from theft and damage'
    },
  ];

  const handlePanelClick = (index) => {
    setActivePanel(index);
  };

  const handleBackClick = () => {
    // Navigate back to the HomePage component
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
    </div>
  );
};

// Simple icon representation using text symbols
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