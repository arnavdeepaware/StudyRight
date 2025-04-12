import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  const handleCreateVideo = (option) => {
    if (option === 'Type your notes') {
      navigate('/notes'); // Navigate to the Notes page
    } else {
      alert(`You selected: ${option}`);
    }
  };

  return (
    <div className="home-container">
      
      <style>{`
        h1 {
          margin-left: 0.75rem;
        }
      `}</style>
    
      <h1>Welcome to StudyRight</h1>

      <div className="recent-reels-container">
        <h2>Recent Reels:</h2>
        <p className="placeholder-text">No recent reels available. Start exploring!</p>
      </div>

      <div className="search-bar-container">
        <span className="search-emoji">🔍</span>
        <input
          type="text"
          className="search-bar"
          placeholder="Find a topic"
        />
      </div>

      <div className="create-video">
        <button onClick={() => handleCreateVideo('Upload a file')}>Upload a file</button>
        <button onClick={() => handleCreateVideo('Type your notes')}>Type your notes</button>
      </div>

    </div>
  );
};

export default HomePage;