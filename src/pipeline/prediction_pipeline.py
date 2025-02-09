import joblib
import pandas as pd
from components.data_transformation import DataTransformation
from utility.util import load_csv

def prediction_pipeline(input_df: pd.DataFrame, artifacts_dir: str):
    # Load the preprocessor
    preprocessor = joblib.load(f'{artifacts_dir}/preprocessor1.pkl')
    scaler = preprocessor['scaler']
    encoder_columns = preprocessor['encoder_columns']

    # Load the trained model
    model = joblib.load(f'{artifacts_dir}/random_forest_model.pkl')

    # Initialize the DataTransformation class
    data_transformation = DataTransformation()

    # Transform the input data for prediction
    input_data_transformed = data_transformation.transform_for_prediction(input_df, scaler, encoder_columns)

    # Make predictions using the loaded model
    predictions = model.predict(input_data_transformed)  # Ensure 'model' is the actual model object

    return predictions

# Example usage
if __name__ == "__main__":
    input_df = load_csv(r'C:\Users\DELL\OneDrive\Desktop\mlops\artifacts\test.csv')  # Load the input data
    predictions = prediction_pipeline(input_df, './artifacts')
    print(predictions)
