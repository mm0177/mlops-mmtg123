import os
import pandas as pd
from utility.util import save_csv
from sklearn.model_selection import train_test_split

def DataIngestion(input_file: str, output_dir: str):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)
    
    # Split the data into train and test sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save train and test dataframes to the artifacts folder
    save_csv(train_df, os.path.join(output_dir, 'train.csv'))
    save_csv(test_df, os.path.join(output_dir, 'test.csv'))
   
    return train_df, test_df

# Example usage
if __name__ == "__main__":
    DataIngestion(r"C:\Users\DELL\OneDrive\Desktop\mlops\train.csv", './artifacts')
