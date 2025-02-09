import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import IntroPage from './components/IntroPage';
import PredictionForm from './components/PredictionForm';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<IntroPage />} />
        <Route path="/predict" element={<PredictionForm />} />
      </Routes>
    </Router>
  );
}

export default App;
