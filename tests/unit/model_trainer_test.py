import os
import pytest
from sklearn.ensemble import RandomForestRegressor
from components.model_trainer import ModelTrainer
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_model_training(tmp_path):
    # Arrange
    train_data = pd.DataFrame({"feature1": [10, 20], "feature2": [1, 2]})
    y_train = pd.Series([100, 200])
    test_data = pd.DataFrame({"feature1": [30], "feature2": [3]})
    y_valid = pd.Series([300])
    model_path = os.path.join(tmp_path, "model.pkl")
    logging.info(f"Temporary directory for model: {tmp_path}")

    # Act
    logging.info("Starting model training...")
    ModelTrainer(train_data, y_train, test_data, y_valid, model_path)
    logging.info("Model training completed.")

    # Assert
    assert os.path.exists(model_path), "Model file was not saved!"
    logging.info(f"Model file successfully saved at: {model_path}")
