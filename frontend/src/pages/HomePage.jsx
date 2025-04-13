import React, { useRef, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [processingStep, setProcessingStep] = useState('');
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  const fileInputRef = useRef(null);
  const leftRef = useRef(null);
  const rightRef = useRef(null);
  const containerRef = useRef(null);

  const processingSteps = [
    { id: 'parse', label: 'Parsing your document...', description: 'Extracting key information from your lecture notes' },
    { id: 'generate', label: 'Generating content...', description: 'Creating visuals and audio for your video' },
    { id: 'render', label: 'Rendering final video...', description: 'Compiling elements into your downloadable video' }
  ];

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

  useEffect(() => {
    let timer;
    if (isLoading) {
      timer = setInterval(() => {
        setCurrentStepIndex((prevIndex) => {
          const newIndex = (prevIndex + 1) % processingSteps.length;
          setProcessingStep(processingSteps[newIndex].label);
          return newIndex;
        });
      }, 1500);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isLoading]);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setMessage(`File selected: ${e.target.files[0].name}`);
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleProcessFile = async () => {
    if (!file) {
      setMessage('Please select a file first');
      return;
    }

    setIsLoading(true);
    setUploadStatus('Transforming your lecture notes into a video');
    setCurrentStepIndex(0);
    setProcessingStep(processingSteps[0].label);
    setMessage('');

    try {
      // STEP 1: Upload document to backend
      const formData = new FormData();
      formData.append('file', file);

      const uploadResponse = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        const errorData = await uploadResponse.json();
        throw new Error(errorData.error || 'File upload failed');
      }

      const uploadData = await uploadResponse.json();

      // STEP 2: Generate video from uploaded file
      const videoResponse = await fetch(`http://localhost:5000/api/video/${uploadData.filename}`, {
        method: 'GET',
      });

      if (!videoResponse.ok) {
        const errorData = await videoResponse.json();
        throw new Error(errorData.error || 'Video generation failed');
      }

      // STEP 3: Upload generated video to S3
      const s3UploadResponse = await fetch('http://localhost:5000/api/upload-from-output', {
        method: 'POST',
      });

      const s3Result = await s3UploadResponse.json();

      if (!s3UploadResponse.ok) {
        throw new Error(s3Result.error || 'S3 upload failed');
      }

      // ✅ DONE: Show video URL
      setMessage(
        <span>
          ✅ Video uploaded!{' '}
          <a href={s3Result.url} target="_blank" rel="noopener noreferrer">
            Watch Video
          </a>
        </span>
      );
    } catch (error) {
      console.error('Error:', error);
      setMessage(`❌ ${error.message}`);
    } finally {
      setIsLoading(false);
      setUploadStatus('');
      setProcessingStep('');
    }
  };

  return (
    <div className="home-container" ref={containerRef}>
      <header className="app-header">
        <div className="logo">
          <span className="logo-icon">SR</span>
          <span className="logo-text">StudyRight</span>
        </div>
        <nav className="nav-menu">
          <button className="nav-button logout" onClick={() => navigate('/')}>
            Logout
          </button>
        </nav>
      </header>

      <div className="split left" ref={leftRef}>
        <div className="content">
          <div className="panel-heading">
            <h1>Your Learning Library</h1>
            <p className="description">Browse and discover content created just for you</p>
          </div>
          <button className="action-btn primary-btn" onClick={() => navigate('/explore')}>
            <span className="btn-icon">🎬</span>
            <span>Explore Videos</span>
          </button>
        </div>
      </div>

      <div className="split right" ref={rightRef}>
        <div className="content">
          <div className="panel-heading">
            <h1>Create New Content</h1>
            <p className="description">Transform your lecture notes into engaging short-form videos</p>
          </div>

          <div className="button-group">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".txt,.pdf,.doc,.docx"
              style={{ display: 'none' }}
            />
            <button className="action-btn upload-btn" onClick={handleUploadClick} disabled={isLoading}>
              <span className="btn-icon">📄</span>
              <span>{isLoading ? 'Processing...' : 'Upload Document'}</span>
            </button>

            {file && (
              <button className="action-btn process-btn" onClick={handleProcessFile} disabled={isLoading}>
                <span className="btn-icon">🚀</span>
                <span>Generate Video</span>
              </button>
            )}

            <button className="action-btn secondary-btn" onClick={() => navigate('/notes')}>
              <span className="btn-icon">✏️</span>
              <span>Type Your Notes</span>
            </button>
          </div>

          {uploadStatus && !isLoading && (
            <div className="status-container">
              <p className="upload-status">{uploadStatus}</p>
              <div className="progress-bar">
                <div className="progress-fill"></div>
              </div>
            </div>
          )}

          {file && (
            <div className="file-info-container">
              <span className="file-icon">📝</span>
              <p className="file-info">{file.name}</p>
            </div>
          )}
        </div>
      </div>

      {message && (
        <div className="message-toast">
          <p>{message}</p>
          <button className="close-toast" onClick={() => setMessage('')}>×</button>
        </div>
      )}

      {isLoading && (
        <div className="loading-overlay">
          <div className="processing-container">
            <div className="loader"><div className="spinner"></div></div>
            <h3 className="processing-title">{uploadStatus}</h3>
            <p className="processing-step">{processingStep}</p>
            <p className="step-description">{processingSteps[currentStepIndex].description}</p>

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

export default HomePage;