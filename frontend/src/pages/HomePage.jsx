import React, { useRef, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

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

  return (
    <div className="container" ref={containerRef}>
      <div className="split left" ref={leftRef}>
        <div className="content">
          <h1>Your Reels</h1>
          <p className="description">Browse and discover amazing content</p>
          <button 
            className="btn" 
            onClick={() => navigate('/explore')}
            aria-label="Explore reels"
          >
            Explore
          </button>
        </div>
      </div>
      <div className="split right" ref={rightRef}>
        <div className="content">
          <h1>Create a Reel</h1>
          <p className="description">Share your creativity with the world</p>
          <div className="button-group">
            <button 
              className="btn" 
              onClick={() => navigate('/upload')}
              aria-label="Upload content for a reel"
            >
              Upload
            </button>
            <button 
              className="btn" 
              onClick={() => navigate('/type-notes')}
              aria-label="Type notes for a reel"
            >
              Type Your Notes
            </button>
          </div>
        </div>
      </div>

      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default HomePage;