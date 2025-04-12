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
      <h1>Welcome to SitRight</h1>
      <div className="create-video">
        <button onClick={() => handleCreateVideo('Upload a file')}>Upload a file</button>
        <button onClick={() => handleCreateVideo('Type your notes')}>Type your notes</button>
      </div>
    </div>
  );
};

export default HomePage;