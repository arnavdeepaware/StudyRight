import React, { useState } from 'react';
import './NotesPage.css';

const NotesPage = () => {
  const [title, setTitle] = useState('');
  const [notes, setNotes] = useState('');

  const handleSave = () => {
    alert(`Video Title: ${title}\nNotes: ${notes}`);
    setTitle('');
    setNotes('');
  };

  return (
    <div className="notes-container">
      <h1>Text Editor</h1>

      <div>
        <h3>Enter your lecture topic:</h3>
        <textarea
          id="video-title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter your video title here..."
          rows="1"
          cols="50"
        ></textarea>
      </div>

      <div>
        <h3>Enter your notes here:</h3>
        <textarea
          id="video-notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Start typing your notes here..."
          rows="10"
          cols="50"
        ></textarea>
      </div>

      <div>
        <button onClick={handleSave}>Generate</button>
      </div>
    </div>
  );
};

export default NotesPage;