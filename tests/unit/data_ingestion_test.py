import pytest
import os
import pandas as pd
from components.data_ingestion import DataIngestion
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_data_ingestion_creates_files(tmp_path):
    # Arrange
    input_file = tmp_path / "input.csv"
    output_dir = tmp_path / "output"
    os.makedirs(output_dir)
    logging.info(f"Temporary directory created at: {tmp_path}")

    # Create mock input data
    input_file.write_text("id,price,feature1\n1,100,10\n2,200,20")
    logging.info(f"Input file written with sample data: {input_file}")

    # Act
    logging.info("Starting DataIngestion process...")
    DataIngestion(input_file=str(input_file), output_dir=str(output_dir))
    logging.info("DataIngestion process completed.")

    # Assert
    train_file = os.path.join(output_dir, "train.csv")
    test_file = os.path.join(output_dir, "test.csv")

    assert os.path.exists(train_file), "Train file was not created!"
    assert os.path.exists(test_file), "Test file was not created!"
    logging.info("Both train and test files are created successfully.")

    # Validate content
    train_data = pd.read_csv(train_file)
    assert not train_data.empty, "Train file is empty!"
    logging.info("Train file content validated.")
