import React from 'react';

const HomePage = () => {
  const handleCreateVideo = (option) => {
    alert(`You selected: ${option}`);
  };

  return (
    <div className="home-container">
      <h1>Welcome to the Home Page</h1>
      <div className="create-video">
        <button onClick={() => handleCreateVideo('Upload a file')}>Upload a file</button>
        <button onClick={() => handleCreateVideo('Type your notes')}>Type your notes</button>
      </div>
    </div>
  );
};

export default HomePage;