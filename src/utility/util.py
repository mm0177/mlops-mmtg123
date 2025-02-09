import os
import pandas as pd
import pickle

def load_csv(file_path: str) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    return pd.read_csv(file_path)

def save_csv(df: pd.DataFrame, file_path: str) -> None:
    """Saves a pandas DataFrame to a CSV file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
def load_artifact(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)
def save_artifact(obj, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)
