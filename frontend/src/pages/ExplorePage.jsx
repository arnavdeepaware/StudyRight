import React from 'react';
import './ExplorePage.css'; // Import the CSS file for styling

const ExplorePage = () => {
  const panels = [
    {
      title: 'Explore The World',
      image: 'https://images.unsplash.com/photo-1558979158-65a1eaa08691?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80',
    },
    {
      title: 'Wild Forest',
      image: 'https://images.unsplash.com/photo-1572276596237-5db2c3e16c5d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80',
    },
    {
      title: 'Sunny Beach',
      image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1353&q=80',
    },
    {
      title: 'City on Winter',
      image: 'https://images.unsplash.com/photo-1551009175-8a68da93d5f9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1351&q=80',
    },
    {
      title: 'Mountains - Clouds',
      image: 'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80',
    },
  ];

  const handlePanelClick = (index) => {
    const panels = document.querySelectorAll('.panel');
    panels.forEach((panel, i) => {
      if (i === index) {
        panel.classList.add('active');
      } else {
        panel.classList.remove('active');
      }
    });
  };

  return (
    <div className="container">
      {panels.map((panel, index) => (
        <div
          key={index}
          className={`panel ${index === 0 ? 'active' : ''}`}
          style={{ backgroundImage: `url(${panel.image})` }}
          onClick={() => handlePanelClick(index)}
        >
          <h3>{panel.title}</h3>
        </div>
      ))}
    </div>
  );
};

export default ExplorePage;