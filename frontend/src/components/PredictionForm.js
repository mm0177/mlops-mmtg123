import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './PredictionForm.css';

function PredictionForm() {
  const [formData, setFormData] = useState({
    carat: '',
    depth: '',
    table: '',
    x: '',
    y: '',
    z: '',
    cut: 'Ideal',
    color: 'D',
    clarity: 'IF',
  });
  const [prediction, setPrediction] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Make a POST request to the Flask API
      const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setPrediction(data.prediction);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div className="prediction-container">
      <h1>Diamond Price Prediction</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="carat">Carat:</label>
        <input type="number" id="carat" name="carat" step="0.01" value={formData.carat} onChange={handleChange} required />

        <label htmlFor="depth">Depth:</label>
        <input type="number" id="depth" name="depth" step="0.01" value={formData.depth} onChange={handleChange} required />

        <label htmlFor="table">Table:</label>
        <input type="number" id="table" name="table" step="0.01" value={formData.table} onChange={handleChange} required />

        <label htmlFor="x">X (Length in mm):</label>
        <input type="number" id="x" name="x" step="0.01" value={formData.x} onChange={handleChange} required />

        <label htmlFor="y">Y (Width in mm):</label>
        <input type="number" id="y" name="y" step="0.01" value={formData.y} onChange={handleChange} required />

        <label htmlFor="z">Z (Depth in mm):</label>
        <input type="number" id="z" name="z" step="0.01" value={formData.z} onChange={handleChange} required />

        <label htmlFor="cut">Cut:</label>
        <select id="cut" name="cut" value={formData.cut} onChange={handleChange} required>
          <option value="Ideal">Ideal</option>
          <option value="Very Good">Very Good</option>
          <option value="Good">Good</option>
          <option value="Fair">Fair</option>
          <option value="Premium">Premium</option>
        </select>

        <label htmlFor="color">Color:</label>
        <select id="color" name="color" value={formData.color} onChange={handleChange} required>
          <option value="D">D</option>
          <option value="E">E</option>
          <option value="F">F</option>
          <option value="G">G</option>
          <option value="H">H</option>
          <option value="I">I</option>
          <option value="J">J</option>
        </select>

        <label htmlFor="clarity">Clarity:</label>
        <select id="clarity" name="clarity" value={formData.clarity} onChange={handleChange} required>
          <option value="IF">IF</option>
          <option value="VVS1">VVS1</option>
          <option value="VVS2">VVS2</option>
          <option value="VS1">VS1</option>
          <option value="VS2">VS2</option>
          <option value="SI1">SI1</option>
          <option value="SI2">SI2</option>
        </select>

        <button type="submit">Predict</button>
      </form>
      {prediction && (
        <div className="prediction">
          <h2>Predicted Price: ${prediction}</h2>
        </div>
      )}
    </div>
  );
}

export default PredictionForm;
