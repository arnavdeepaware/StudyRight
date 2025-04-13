import React, { useEffect, useState } from 'react';
import axios from 'axios';

const VideoGallery = ({ userId }) => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/api/videos/${userId}`)
      .then((res) => setVideos(res.data.videos))
      .catch((err) => console.error(err));
  }, [userId]);

  return (
    <div>
      <h2>Videos for User: {userId}</h2>
      {videos.length === 0 ? (
        <p>No videos found.</p>
      ) : (
        videos.map((video) => (
          <div key={video._id}>
            <h4>{video.filename}</h4>
            <video src={video.video_url} controls width="480" />
          </div>
        ))
      )}
    </div>
  );
};

export default VideoGallery;