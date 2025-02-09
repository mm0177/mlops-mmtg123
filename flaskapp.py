from flask import Flask, render_template, request
import joblib
import pandas as pd
from components.data_transformation import DataTransformation
from utility.util import load_csv
from pipeline.prediction_pipeline import prediction_pipeline  # Import the prediction pipeline

app = Flask(__name__)

# Define the route to handle predictions
@app.route('/', methods=['GET', 'POST'])
def predict():
    prediction = None

    if request.method == 'POST':
        # Get data from the form
        input_data = {
            'carat': float(request.form['carat']),
            'depth': float(request.form['depth']),
            'table': float(request.form['table']),
            'x': float(request.form['x']),
            'y': float(request.form['y']),
            'z': float(request.form['z']),
            'cut': request.form['cut'],
            'color': request.form['color'],
            'clarity': request.form['clarity']
        }

        # Convert the input data into a DataFrame
        input_df = pd.DataFrame([input_data])

        # Define the path to the artifacts
        artifacts_dir = './artifacts'

        # Call the prediction pipeline to get the prediction
        predictions = prediction_pipeline(input_df, artifacts_dir)

        # Get the predicted price (assuming it's a single prediction)
        prediction = predictions[0]

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
