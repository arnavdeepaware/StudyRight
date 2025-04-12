import React, { useEffect } from 'react';
import './HomePage.css';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  useEffect(() => {
    const left = document.querySelector('.left');
    const right = document.querySelector('.right');
    const container = document.querySelector('.container');

    const addHoverLeft = () => container.classList.add('hover-left');
    const removeHoverLeft = () => container.classList.remove('hover-left');

    const addHoverRight = () => container.classList.add('hover-right');
    const removeHoverRight = () => container.classList.remove('hover-right');

    left.addEventListener('mouseenter', addHoverLeft);
    left.addEventListener('mouseleave', removeHoverLeft);
    right.addEventListener('mouseenter', addHoverRight);
    right.addEventListener('mouseleave', removeHoverRight);

    return () => {
      left.removeEventListener('mouseenter', addHoverLeft);
      left.removeEventListener('mouseleave', removeHoverLeft);
      right.removeEventListener('mouseenter', addHoverRight);
      right.removeEventListener('mouseleave', removeHoverRight);
    };
  }, []);

  return (
    <div className="container">
      <div className="split left">
        <h1>Your Reels</h1>
        <button className="btn" onClick={() => navigate('/explore')}>Explore</button>
      </div>
      <div className="split right">
        <h1>Create a Reel</h1>
        <button className="btn" onClick={() => navigate('/notes')}>Start Now</button>
      </div>
    </div>
  );
};

export default HomePage;