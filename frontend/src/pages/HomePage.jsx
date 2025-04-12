import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleCreateVideo = async (option) => {
    if (option === 'Type your notes') {
      navigate('/notes'); // Navigate to the Notes page
    } else if (option === 'Upload a file') {
      if (!file) {
        setMessage('Please select a file first');
        return;
      }

      setUploading(true);
      setMessage('Uploading file...');
      
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://127.0.0.1:5000/api/upload', {
          method: 'POST',
          body: formData,
        });

        const data = await response.json();
        
        if (response.ok) {
          setMessage('File uploaded successfully!');
          // You can navigate to a success page or do something with the response
        } else {
          setMessage(`Error: ${data.error}`);
        }
      } catch (error) {
        setMessage(`Error uploading file: ${error.message}`);
      } finally {
        setUploading(false);
      }
    }
  };

  return (
    <div className="home-container">
      <h1>Welcome to SitRight</h1>
      
      <div className="file-upload">
        <input type="file" onChange={handleFileChange} />
      </div>
      
      <div className="create-video">
        <button 
          onClick={() => handleCreateVideo('Upload a file')}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Upload a file'}
        </button>
        <button onClick={() => handleCreateVideo('Type your notes')}>Type your notes</button>
      </div>
      
      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default HomePage;