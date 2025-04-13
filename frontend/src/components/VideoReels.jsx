import React, { useState, useEffect, useRef } from 'react';
import './VideoReels.css';

const VideoReels = () => {
  const [videos, setVideos] = useState([]);
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(true);
  const videoRefs = useRef([]);
  
  // Generate mock data for demo
  useEffect(() => {
    const mockVideos = Array(10).fill().map((_, index) => ({
      id: `video-${index}`,
      title: `Learning Concept #${index + 1}`,
      description: 'This is a short educational video explaining a key concept from your lecture notes.',
      videoUrl: [
        'https://samplelib.com/lib/preview/mp4/sample-5s.mp4',
        'https://samplelib.com/lib/preview/mp4/sample-10s.mp4',
        'https://samplelib.com/lib/preview/mp4/sample-15s.mp4',
        'https://samplelib.com/lib/preview/mp4/sample-20s.mp4',
        'https://samplelib.com/lib/preview/mp4/sample-30s.mp4'
      ][index % 5], // Cycle through sample videos
      likes: Math.floor(Math.random() * 1000) + 100,
      shares: Math.floor(Math.random() * 100) + 10,
      user: {
        name: `Student ${index + 1}`,
        avatar: `https://i.pravatar.cc/150?img=${index % 70}`
      }
    }));
    
    setVideos(mockVideos);
    setIsLoading(false);
  }, []);
  
  // Handle video interactions
  const togglePlayPause = () => {
    const video = videoRefs.current[currentVideoIndex];
    if (!video) return;
    
    if (video.paused) {
      video.play();
      setIsPlaying(true);
    } else {
      video.pause();
      setIsPlaying(false);
    }
  };
  
  // Handle scroll to next/previous video
  const handleScroll = (direction) => {
    const newIndex = direction === 'left' 
      ? Math.max(0, currentVideoIndex - 1)
      : Math.min(videos.length - 1, currentVideoIndex + 1);
    
    if (newIndex !== currentVideoIndex) {
      // Pause current video
      if (videoRefs.current[currentVideoIndex]) {
        videoRefs.current[currentVideoIndex].pause();
      }
      
      setCurrentVideoIndex(newIndex);
      
      // Play new video after a short delay
      setTimeout(() => {
        if (videoRefs.current[newIndex]) {
          videoRefs.current[newIndex].play();
          setIsPlaying(true);
        }
      }, 10);
    }
  };
  
  // Handle swipe gesture
  const [touchStart, setTouchStart] = useState(null);
  const [touchEnd, setTouchEnd] = useState(null);
  
  const handleTouchStart = (e) => {
    setTouchStart(e.targetTouches[0].clientX);
  };
  
  const handleTouchMove = (e) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };
  
  const handleTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isSwipeRight = distance > 50;
    const isSwipeLeft = distance < -50;
    
    if (isSwipeRight) {
      handleScroll('right');
    } else if (isSwipeLeft) {
      handleScroll('left');
    }
    
    setTouchStart(null);
    setTouchEnd(null);
  };
  
  // Handle video ended - auto advance
  const handleVideoEnded = () => {
    if (currentVideoIndex < videos.length - 1) {
      handleScroll('right');
    } else {
      // We're at the last video, loop back to first
      setCurrentVideoIndex(0);
      setTimeout(() => {
        if (videoRefs.current[0]) {
          videoRefs.current[0].play();
        }
      }, 10);
    }
  };
  
  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowLeft') {
        handleScroll('left');
      } else if (e.key === 'ArrowRight') {
        handleScroll('right');
      } else if (e.key === ' ') {
        togglePlayPause();
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [currentVideoIndex]);
  
  // Playing/pausing the current video when index changes
  useEffect(() => {
    videoRefs.current.forEach((video, index) => {
      if (!video) return;
      
      if (index === currentVideoIndex) {
        video.currentTime = 0;
        video.play().catch(err => console.error('Error playing video:', err));
        setIsPlaying(true);
      } else {
        video.pause();
        video.currentTime = 0;
      }
    });
  }, [currentVideoIndex]);
  
  const handleLike = (videoId) => {
    setVideos(prevVideos => 
      prevVideos.map(video => 
        video.id === videoId 
          ? { ...video, likes: video.hasLiked ? video.likes - 1 : video.likes + 1, hasLiked: !video.hasLiked } 
          : video
      )
    );
  };
  
  const handleShare = (video) => {
    // In a real implementation, this would open a share dialog
    // For now, we'll show an alert and increase the share count
    alert(`Sharing video: ${video.title}`);
    
    // Increase share count
    setVideos(prevVideos => 
      prevVideos.map(v => 
        v.id === video.id 
          ? { ...v, shares: v.shares + 1 } 
          : v
      )
    );
    
    // Web Share API if available
    if (navigator.share) {
      navigator.share({
        title: video.title,
        text: video.description,
        url: window.location.href,
      }).catch(console.error);
    }
  };
  
  // Quiz interaction (simplified example)
  const [showQuiz, setShowQuiz] = useState(false);
  const [quizAnswered, setQuizAnswered] = useState(false);
  const [quizCorrect, setQuizCorrect] = useState(false);
  
  const handleQuizToggle = () => {
    setShowQuiz(!showQuiz);
    if (showQuiz) {
      setQuizAnswered(false);
      setQuizCorrect(false);
    }
  };
  
  const handleQuizAnswer = (isCorrect) => {
    setQuizAnswered(true);
    setQuizCorrect(isCorrect);
    
    // Pause video when showing quiz result
    if (videoRefs.current[currentVideoIndex]) {
      videoRefs.current[currentVideoIndex].pause();
      setIsPlaying(false);
    }
  };
  
  return (
    <div 
      className="video-reels"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      {isLoading ? (
        <div className="reels-loading">
          <div className="spinner"></div>
          <p>Loading videos...</p>
        </div>
      ) : (
        <>
          <div className="reels-container">
            {videos.map((video, index) => (
              <div 
                key={video.id} 
                className={`reel-item ${index === currentVideoIndex ? 'active' : ''}`}
                style={{transform: `translateX(${(index - currentVideoIndex) * 100}%)`}}
              >
                <div className="video-wrapper">
                  <video
                    ref={el => videoRefs.current[index] = el}
                    src={video.videoUrl}
                    loop={false}
                    muted={false}
                    playsInline
                    onClick={togglePlayPause}
                    onEnded={handleVideoEnded}
                    className="reel-video"
                  />
                  
                  {!isPlaying && index === currentVideoIndex && (
                    <div className="play-overlay" onClick={togglePlayPause}>
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 5V19L19 12L8 5Z" fill="currentColor" />
                      </svg>
                    </div>
                  )}
                  
                  <div className="reel-overlay">
                    <div className="reel-info">
                      <div className="reel-user">
                        <img src={video.user.avatar} alt={video.user.name} className="user-avatar" />
                        <span className="user-name">{video.user.name}</span>
                      </div>
                      <h3 className="reel-title">{video.title}</h3>
                      <p className="reel-description">{video.description}</p>
                    </div>
                    
                    <div className="reel-actions">
                      <button 
                        className={`action-button ${video.hasLiked ? 'active' : ''}`}
                        onClick={() => handleLike(video.id)}
                      >
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="currentColor" />
                        </svg>
                        <span>{video.likes}</span>
                      </button>
                      
                      <button 
                        className="action-button"
                        onClick={() => handleShare(video)}
                      >
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7 0-.24-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92 0-1.61-1.31-2.92-2.92-2.92z" fill="currentColor" />
                        </svg>
                        <span>{video.shares}</span>
                      </button>
                      
                      <button 
                        className={`action-button ${showQuiz ? 'active' : ''}`}
                        onClick={handleQuizToggle}
                      >
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm0-4h-2V7h2v8z" fill="currentColor" />
                        </svg>
                        <span>Quiz</span>
                      </button>
                    </div>
                  </div>
                </div>
                
                {showQuiz && index === currentVideoIndex && (
                  <div className="quiz-overlay">
                    <div className="quiz-container">
                      <button className="close-quiz" onClick={handleQuizToggle}>×</button>
                      
                      {!quizAnswered ? (
                        <>
                          <h3>Quick Check</h3>
                          <p>What is the main concept explained in this video?</p>
                          
                          <div className="quiz-options">
                            <button onClick={() => handleQuizAnswer(true)}>The correct answer</button>
                            <button onClick={() => handleQuizAnswer(false)}>An incorrect option</button>
                            <button onClick={() => handleQuizAnswer(false)}>Another wrong choice</button>
                          </div>
                        </>
                      ) : (
                        <div className={`quiz-result ${quizCorrect ? 'correct' : 'incorrect'}`}>
                          <div className="result-icon">
                            {quizCorrect ? '✓' : '✗'}
                          </div>
                          <h3>{quizCorrect ? 'Correct!' : 'Not quite!'}</h3>
                          <p>
                            {quizCorrect 
                              ? 'Great job! You understood the key concept.' 
                              : 'The correct answer is "The correct answer". Try watching the video again.'}
                          </p>
                          <button className="continue-btn" onClick={handleQuizToggle}>Continue</button>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
          
          <div className="navigation-indicators">
            {videos.map((_, index) => (
              <div 
                key={index} 
                className={`nav-dot ${index === currentVideoIndex ? 'active' : ''}`}
                onClick={() => {
                  setCurrentVideoIndex(index);
                }}
              />
            ))}
          </div>
          
          <div className="navigation-arrows">
            <button 
              className={`nav-arrow left ${currentVideoIndex === 0 ? 'disabled' : ''}`}
              onClick={() => handleScroll('left')}
              disabled={currentVideoIndex === 0}
              aria-label="Previous video"
            >
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" fill="currentColor" />
              </svg>
            </button>
            
            <button 
              className={`nav-arrow right ${currentVideoIndex === videos.length - 1 ? 'disabled' : ''}`}
              onClick={() => handleScroll('right')}
              disabled={currentVideoIndex === videos.length - 1}
              aria-label="Next video"
            >
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" fill="currentColor" />
              </svg>
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default VideoReels;