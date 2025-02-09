import os
from pipeline.prediction_pipeline import PredictionPipeline

# Define paths to the trained model and preprocessor
model_path = './artifacts/random_forest_model.pkl'
preprocessor_path = './artifacts/preprocessor1.pkl'

# Check if the necessary files exist
if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
    raise FileNotFoundError("Model or preprocessor file is missing. Ensure you have trained the model and saved the preprocessor.")

# Initialize the PredictionPipeline
try:
    print("Initializing the PredictionPipeline...")
    pipeline = PredictionPipeline(model_path, preprocessor_path)
    print("Pipeline initialized successfully.")
except Exception as e:
    print(f"Error during pipeline initialization: {e}")
    raise

# Sample input data for testing
sample_input = {
    "carat": 0.5,
    "cut": "Ideal",
    "color": "E",
    "clarity": "VS1",
    "depth": 61.8,
    "table": 57.0,
    "x": 5.1,
    "y": 5.15,
    "z": 3.2
}

# Predict using the pipeline
try:
    print("Predicting with sample input...")
    prediction = pipeline.predict(sample_input)
    print(f"Predicted Price: ${prediction:.2f}")
except Exception as e:
    print(f"An error occurred during prediction: {e}")
