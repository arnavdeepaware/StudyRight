import React, { useState } from 'react';

const NotesPage = () => {
  const [title, setTitle] = useState(''); // State for video title
  const [notes, setNotes] = useState(''); // State for notes

  const handleSave = () => {
    alert(`Video Title: ${title}\nNotes: ${notes}`);
    setTitle(''); // Clear the title after saving
    setNotes(''); // Clear the notes after saving
  };

  return (
    <div className="notes-container">
      
      <h1>Text/Script Editor</h1>

      <div>
        <h3>Enter your video title:</h3>
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
        <button onClick={handleSave}>Generate Reels</button>
      </div>

    </div>
  );
};

export default NotesPage;