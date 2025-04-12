import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import NotesPage from './pages/NotesPage';
import ExplorePage from './pages/ExplorePage'; // Import the ExplorePage
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/notes" element={<NotesPage />} />
        <Route path="/explore" element={<ExplorePage />} /> {/* Add the ExplorePage route */}
      </Routes>
    </Router>
  </React.StrictMode>
);