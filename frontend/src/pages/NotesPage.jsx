import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './NotesPage.css';

const NotesPage = () => {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [notes, setNotes] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [uploadStatus, setUploadStatus] = useState('');
  const [processingStep, setProcessingStep] = useState('');
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  
  const titleInputRef = useRef(null);
  
  // Focus on title input when component mounts
  useEffect(() => {
    if (titleInputRef.current) {
      titleInputRef.current.focus();
    }
  }, []);
  
  // Processing steps for the animation
  const processingSteps = [
    { id: 'parse', label: 'Parsing your notes...', description: 'Extracting key information from your lecture notes' },
    { id: 'generate', label: 'Generating content...', description: 'Creating visuals and audio for your video' },
    { id: 'render', label: 'Rendering final video...', description: 'Compiling elements into your downloadable video' }
  ];

  // Animated progression through processing steps
  useEffect(() => {
    let timer;
    if (isLoading) {
      timer = setInterval(() => {
        setCurrentStepIndex(prevIndex => {
          const newIndex = (prevIndex + 1) % processingSteps.length;
          setProcessingStep(processingSteps[newIndex].label);
          return newIndex;
        });
      }, 1500);
    }

    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isLoading, processingSteps]);

  const handleGenerate = async () => {
    console.log('Generate button clicked');

    if (!title.trim() || !notes.trim()) {
      setMessage('Please enter both a title and notes.');
      return;
    }

    setIsLoading(true);
    setUploadStatus('Creating your video from notes');
    setProcessingStep(processingSteps[0].label);
    setCurrentStepIndex(0);
    setMessage('');

    try {
      // Create a text file from the notes
      const content = `# ${title}\n\n${notes}`;
      const file = new File([content], `${title.replace(/\s+/g, '_')}.txt`, { type: 'text/plain' });
      
      console.log('Attempting to upload file:', file);

      // Step 1: Upload the file using the existing API
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
      
      // Step 2: Generate video from the uploaded file
      const videoResponse = await fetch(`http://localhost:8080/api/video/${uploadData.filename}`, {
        method: 'GET',
      });

      if (!videoResponse.ok) {
        const errorData = await videoResponse.json();
        throw new Error(errorData.error || 'Video generation failed');
      }

      // Create a blob URL for the video and download it
      const videoBlob = await videoResponse.blob();
      const url = URL.createObjectURL(videoBlob);
      
      // Trigger automatic download
      const fileName = `${title.replace(/\s+/g, '_')}_video.mp4`;
      const downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.download = fileName;
      downloadLink.style.display = 'none';
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
      
      // Clean up the blob URL after download
      setTimeout(() => {
        URL.revokeObjectURL(url);
      }, 100);
      
      setMessage(`Success! Your video "${fileName}" has been downloaded.`);
      
      // Reset the form after successful generation
      setTitle('');
      setNotes('');
    } catch (error) {
      console.error('Error:', error);
      setMessage(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
      setUploadStatus('');
      setProcessingStep('');
    }
  };

  return (
    <div className="notes-page">
      <header className="app-header">
        <div className="logo" onClick={() => navigate('/')}>
          <span className="logo-icon">SR</span>
          <span className="logo-text">StudyRight</span>
        </div>
        <nav className="nav-menu">
          <button className="nav-button" onClick={() => navigate('/')}>Home</button>
          <button className="nav-button" onClick={() => navigate('/explore')}>Explore</button>
          <button className="nav-button logout" onClick={() => navigate('/login')}>Logout</button>
        </nav>
      </header>
      
      <div className="main-content">
        {/* Sidebar now takes full height */}
        <div className="editor-sidebar">
          <h2>Create Study Video</h2>
          <p className="sidebar-text">Enter your notes and our AI will convert them into an engaging video for better learning retention.</p>
          
          <div className="sidebar-tips">
            <h3>Tips</h3>
            <ul>
              <li>Be clear and concise with your notes</li>
              <li>Include key concepts and definitions</li>
              <li>Add examples to illustrate points</li>
              <li>Structure content with clear sections</li>
            </ul>
          </div>
          
          <div className="generate-btn-container">
            <button 
              className="generate-btn" 
              onClick={handleGenerate}
              disabled={isLoading || !title.trim() || !notes.trim()}
              type="button"
            >
              {isLoading ? 'Processing...' : 'Generate Video'}
            </button>
            
            {(!title.trim() || !notes.trim()) && !isLoading && (
              <div className="btn-hint">
                {!title.trim() ? "Please enter a title" : "Please enter your notes"}
              </div>
            )}
          </div>
        </div>
        
        {/* Right side contains both title and notes input */}
        <div className="editor-content">
          <div className="title-container">
            <input
              ref={titleInputRef}
              className="title-input"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter lecture title..."
              disabled={isLoading}
            />
          </div>
          
          <div className="editor-main">
            <textarea
              className="notes-input"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Type or paste your lecture notes here..."
              disabled={isLoading}
            ></textarea>
          </div>
        </div>
      </div>

      {message && (
        <div className="message-toast">
          <p>{message}</p>
          <button className="close-toast" onClick={() => setMessage('')}>×</button>
        </div>
      )}

      {/* Loading overlay with processing steps */}
      {isLoading && (
        <div className="loading-overlay">
          <div className="processing-container">
            <div className="loader">
              <div className="spinner"></div>
            </div>
            <h3 className="processing-title">{uploadStatus}</h3>
            <p className="processing-step">{processingStep}</p>
            
            <div className="processing-steps">
              {processingSteps.map((step, index) => (
                <React.Fragment key={step.id}>
                  <div className={`step-indicator ${index <= currentStepIndex ? 'active' : ''}`}>
                    <div className="step-ball"></div>
                    <span>{step.id.charAt(0).toUpperCase() + step.id.slice(1)}</span>
                  </div>
                  {index < processingSteps.length - 1 && (
                    <div className={`step-line ${index < currentStepIndex ? 'active' : ''}`}></div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NotesPage;