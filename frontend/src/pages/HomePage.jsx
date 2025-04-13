import React, { useRef, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [file, setFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const leftRef = useRef(null);
  const rightRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const left = leftRef.current;
    const right = rightRef.current;
    const container = containerRef.current;

    if (!left || !right || !container) return;

    const addHoverLeft = () => container.classList.add('hover-left');
    const removeHoverLeft = () => container.classList.remove('hover-left');

    const addHoverRight = () => container.classList.add('hover-right');
    const removeHoverRight = () => container.classList.remove('hover-right');

    left.addEventListener('mouseenter', addHoverLeft);
    left.addEventListener('mouseleave', removeHoverLeft);
    right.addEventListener('mouseenter', addHoverRight);
    right.addEventListener('mouseleave', removeHoverRight);

    const handleKeyDown = (e) => {
      if (e.key === 'ArrowLeft') addHoverLeft();
      if (e.key === 'ArrowRight') addHoverRight();
      if (e.key === 'Escape') {
        removeHoverLeft();
        removeHoverRight();
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      left.removeEventListener('mouseenter', addHoverLeft);
      left.removeEventListener('mouseleave', removeHoverLeft);
      right.removeEventListener('mouseenter', addHoverRight);
      right.removeEventListener('mouseleave', removeHoverRight);
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  // Handle file selection
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setMessage(`File selected: ${e.target.files[0].name}`);
    }
  };

  // Trigger file input click
  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  // Process the selected file
  const handleProcessFile = async () => {
    if (!file) {
      setMessage('Please select a file first');
      return;
    }

    // Reset states
    setIsLoading(true);
    setUploadStatus('Uploading your file...');
    setMessage('');
    setVideoUrl(null);

    try {
      // Step 1: Upload the file
      const formData = new FormData();
      formData.append('file', file);

      const uploadResponse = await fetch('http://localhost:8080/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        const errorData = await uploadResponse.json();
        throw new Error(errorData.error || 'File upload failed');
      }

      const uploadData = await uploadResponse.json();
      setUploadStatus('Processing your file into a video...');
      
      // Step 2: Generate video from the uploaded file
      const videoResponse = await fetch(`http://localhost:8080/api/video/${uploadData.filename}`, {
        method: 'GET',
      });

      if (!videoResponse.ok) {
        const errorData = await videoResponse.json();
        throw new Error(errorData.error || 'Video generation failed');
      }

      // Create a blob URL for the video
      const videoBlob = await videoResponse.blob();
      const url = URL.createObjectURL(videoBlob);
      setVideoUrl(url);
      setUploadStatus('Video generated successfully!');
      
      // Open the video in a new window
      const newWindow = window.open('', '_blank');
      if (newWindow) {
        newWindow.document.write(`
          <!DOCTYPE html>
          <html>
            <head>
              <title>Generated Video</title>
              <style>
                body {
                  margin: 0;
                  padding: 0;
                  background-color: #000;
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  height: 100vh;
                  overflow: hidden;
                }
                video {
                  max-width: 90%;
                  max-height: 90vh;
                  box-shadow: 0 0 20px rgba(0,0,0,0.5);
                }
                h1 {
                  color: white;
                  font-family: Arial, sans-serif;
                  position: absolute;
                  top: 10px;
                  left: 20px;
                }
                .info {
                  color: #ccc;
                  font-family: Arial, sans-serif;
                  position: absolute;
                  bottom: 10px;
                  left: 20px;
                }
              </style>
            </head>
            <body>
              <h1>Your Generated Video</h1>
              <video controls autoplay>
                <source src="${url}" type="video/mp4">
                Your browser does not support the video tag.
              </video>
              <div class="info">Generated from: ${file.name}</div>
              <script>
                // Keep the blob URL valid even after this window is closed
                window.addEventListener('beforeunload', function() {
                  window.opener.postMessage({ type: 'VIDEO_WINDOW_CLOSED' }, '*');
                });
              </script>
            </body>
          </html>
        `);
        newWindow.document.close();
      } else {
        // If popup is blocked, show a message and keep the embedded video player
        setMessage('Popup blocked. Please allow popups to open video in a new window.');
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage(`Error: ${error.message}`);
      setUploadStatus('');
    } finally {
      setIsLoading(false);
    }
  };

  // Add an event listener to handle messages from the popup window
  useEffect(() => {
    const handleMessage = (event) => {
      if (event.data.type === 'VIDEO_WINDOW_CLOSED') {
        // Optionally clean up when video window is closed
        URL.revokeObjectURL(videoUrl);
      }
    };
    
    window.addEventListener('message', handleMessage);
    return () => {
      window.removeEventListener('message', handleMessage);
    };
  }, [videoUrl]);

  return (
    <div className="container" ref={containerRef}>
      <div className="split left" ref={leftRef}>
        <div className="content">
          <h1>Your Videos</h1>
          <p className="description">Browse and discover amazing content</p>
          <button 
            className="btn" 
            onClick={() => navigate('/explore')}
            aria-label="Explore reels"
          >
            Explore
          </button>
          
          {/* Video player section */}
          {videoUrl && (
            <div className="video-container">
              <video 
                ref={videoRef}
                controls
                width="100%"
                className="result-video"
              >
                <source src={videoUrl} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          )}
        </div>
      </div>
      
      <div className="split right" ref={rightRef}>
        <div className="content">
          <h1>Create a Video</h1>
          <p className="description">Share your creativity with the world</p>
          
          {/* File upload section */}
          <div className="button-group">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".txt,.pdf,.doc,.docx"
              style={{ display: 'none' }}
            />
            <button 
              className="btn" 
              onClick={handleUploadClick}
              aria-label="Upload content for a reel"
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Upload File'}
            </button>
            
            {file && (
              <button 
                className="btn process-btn" 
                onClick={handleProcessFile}
                disabled={isLoading}
              >
                Process File
              </button>
            )}
            
            <button 
              className="btn" 
              onClick={() => navigate('/notes')}
              aria-label="Type notes for a reel"
            >
              Type Your Notes
            </button>
          </div>
          
          {/* Status messages */}
          {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
          {file && <p className="file-info">Selected: {file.name}</p>}
        </div>
      </div>

      {message && <p className="message">{message}</p>}
      
      {/* Loading indicator */}
      {isLoading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>{uploadStatus}</p>
        </div>
      )}
    </div>
  );
};

export default HomePage;