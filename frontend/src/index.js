import React from 'react';
import { createRoot } from 'react-dom/client';  // ✅ Correct import
import App from './App'; // ✅ Match the correct filename
import './App.css';

const root = createRoot(document.getElementById('root')); // ✅ Correct way in React 19
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
