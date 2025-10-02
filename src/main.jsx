import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './HashGenerator.jsx'; 

// This file is the standard entry point for a modern React application.
// We are importing the main 'App' component from the same directory (./)
// because the HashGenerator.jsx file should be located inside the src/ folder.
// NOTE: The explicit .jsx extension is now included to resolve the module resolution error.

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
