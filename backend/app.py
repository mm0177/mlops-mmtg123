# backend/app.py
from flask import Flask, render_template, request, send_from_directory, jsonify,make_response
import os
import pandas as pd
from pipeline.prediction_pipeline import prediction_pipeline
import joblib
import pandas as pd
from components.data_transformation import DataTransformation
from utility.util import load_csv

# Create the Flask app, pointing to the React build for templates and static files
app = Flask(__name__, template_folder='build', static_folder='build/static')

# Serve the React application for non-API routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.template_folder, path)):
        return send_from_directory(app.template_folder, path)
    else:
        return send_from_directory(app.template_folder, 'index.html')

# API endpoint for predictions
@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 🛠️ Get JSON data
        data = request.get_json()
        print("Received JSON data:", data)  # Debugging

        required_fields = ['carat', 'depth', 'table', 'x', 'y', 'z', 'cut', 'color', 'clarity']
        
        # 🛠️ Ensure all fields exist
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {missing_fields}'}), 400
        
        # 🛠️ Convert data types
        try:
            processed_data = {
                'carat': float(data['carat']),
                'depth': float(data['depth']),
                'table': float(data['table']),
                'x': float(data['x']),
                'y': float(data['y']),
                'z': float(data['z']),
                'cut': data['cut'],  # Categorical
                'color': data['color'],  # Categorical
                'clarity': data['clarity']  # Categorical
            }
        except ValueError as e:
            return jsonify({'error': f'Invalid data format: {str(e)}'}), 400

        # 🛠️ Convert to DataFrame
        input_df = pd.DataFrame([processed_data])
        print("Converted DataFrame:", input_df)  # Debugging

        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        artifacts_dir = os.path.join(BASE_DIR, "artifacts")

        print("Artifacts directory:", artifacts_dir) 

        # 🛠️ Call the prediction pipeline
        predictions = prediction_pipeline(input_df, artifacts_dir)
        # Prevent browser caching
        response = make_response(jsonify({'prediction': predictions[0]}))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'


        return response

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
