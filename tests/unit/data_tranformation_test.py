import pytest
import pandas as pd
from components.data_transformation import DataTransformation
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_data_transformation():
    # Arrange
    train_data = pd.DataFrame({
        "price": [100, 200],
        "feature1": [10, 20],
        "id": [1, 2]
    })
    test_data = pd.DataFrame({
        "price": [300],
        "feature1": [30],
        "id": [3]
    })

    logging.info("Setting up data for transformation test.")

    data_transformation = DataTransformation()

    # Act
    logging.info("Starting data transformation...")
    train_transformed, test_transformed = data_transformation.initiate_data_transformation(
        train_data.drop(columns=["price", "id"]),
        test_data.drop(columns=["price", "id"])
    )
    logging.info("Data transformation completed.")

    # Assert
    assert train_transformed.shape[0] == 2, "Train data rows mismatch!"
    assert test_transformed.shape[0] == 1, "Test data rows mismatch!"
    assert "feature1" in train_transformed.columns, "Transformed column missing!"
    logging.info("Data transformation test passed.")
