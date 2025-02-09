import os
import pandas as pd
from components.data_ingestion import DataIngestion
from components.data_transformation import DataTransformation
from components.model_trainer import ModelTrainer
from utility.util import load_csv, save_artifact
import mlflow


def training_pipeline(artifacts_dir: str):
    # Ensure the artifacts directory exists
    os.makedirs(artifacts_dir, exist_ok=True)
    
    # Default path for the raw data
    raw_data_dir = './artifacts'
    raw_data_file = os.path.join(raw_data_dir, 'train.csv')
    
    # Check if the raw data file exists
    if not os.path.exists(raw_data_file):
        raise FileNotFoundError(f"Raw data file not found at {raw_data_file}. Please provide the input data.")
    
    # File paths for train and test CSVs
    train_file_path = os.path.join(artifacts_dir, 'train.csv')
    test_file_path = os.path.join(artifacts_dir, 'test.csv')
    
    # Step 1: Data Ingestion
    if not os.path.exists(train_file_path) or not os.path.exists(test_file_path):
        print("Train or test files not found. Running data ingestion step...")
        DataIngestion(input_file=raw_data_file, output_dir=artifacts_dir)
    
    # Step 2: Load the data
    train_df = load_csv(train_file_path)
    test_df = load_csv(test_file_path)
    data_transformation = DataTransformation()
    
    # Step 3: Data Transformation
    # Separate the target variable 'price' before applying transformations
    y_train = train_df['price']
    y_valid = test_df['price']
    
    # Now drop the 'price' column from train_df and test_df before applying transformation
    train_df = train_df.drop(columns=['price','id'])
    test_df = test_df.drop(columns=['price','id'])
    
    # Apply transformations (e.g., encoding, scaling)
    train_df_transformed, test_df_transformed = data_transformation.initiate_data_transformation(train_df, test_df)

    # Save the column names for later use in prediction pipeline
    transformed_columns = train_df_transformed.columns
    save_artifact(transformed_columns, os.path.join(artifacts_dir, 'transformed_columns.pkl'))


    mlflow.set_experiment("Price Prediction")


    with mlflow.start_run(run_name="Training"):
        mlflow.log_param("num_train_samples",train_df_transformed.shape[0])
        mlflow.log_param("num_test_samples",test_df_transformed.shape[0])
        mlflow.log_param("features",list(train_df_transformed.columns))
        
        model, mse, rmse, r2 = ModelTrainer(
        train_df_transformed, y_train, test_df_transformed, y_valid,
        os.path.join(artifacts_dir, 'random_forest_model.pkl')
        )
        mlflow.log_metric("mse",mse)
        mlflow.log_metric("rmse",rmse)
        mlflow.log_metric("r2",r2)
        
        
        scaler = data_transformation.scaler
        encoder = data_transformation.encoder
        save_artifact(scaler, os.path.join(artifacts_dir, 'scaler.pkl'))
        save_artifact(encoder, os.path.join(artifacts_dir, 'encoder.pkl'))



        mlflow.sklearn.log_model(model,"model")
        mlflow.log_artifact(os.path.join(artifacts_dir,'scaler.pkl'))
        mlflow.log_artifact(os.path.join(artifacts_dir,'encoder.pkl'))
        mlflow.log_artifact(os.path.join(artifacts_dir,'transformed_columns.pkl'))


        print(f"Metrics logged to Mlflow :RMSE:{rmse}, R2: {r2}")
    
    
    return model, mse, rmse, r2

# Example usage
if __name__ == "__main__":
    model, mse, rmse, r2 = training_pipeline('./artifacts')
    print(f"Model training completed. RMSE: {rmse}, R2: {r2}")
