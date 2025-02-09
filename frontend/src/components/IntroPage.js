import React from 'react';
import { useNavigate } from 'react-router-dom';
import './IntroPage.css';

function IntroPage() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/predict');
  };

  return (
    <div className="intro-container">
      <div className="content">
        <h1>🔮 Gemstone Price Predictor 💎</h1>
        <p>
          Harness the power of AI to predict gemstone prices based on quality and characteristics.
          Enter the details and get instant insights!
        </p>
        <button onClick={handleGetStarted}>✨ Get Started</button>
      </div>
    </div>
  );
}

export default IntroPage;
