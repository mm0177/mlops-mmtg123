import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

class DataTransformation:
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = None  # Placeholder for one-hot encoder
        self.columns = None  # Placeholder for all columns after encoding
    
    def initiate_data_transformation(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        # Separate numeric and categorical columns
        numerical_cols = train_df.select_dtypes(include=['float64', 'int64']).columns
        categorical_cols = train_df.select_dtypes(include=['object']).columns
        
        # Fill missing values for numerical columns with the median
        for col in numerical_cols:
            train_df[col] = train_df[col].fillna(train_df[col].median())
            test_df[col] = test_df[col].fillna(test_df[col].median())
        
        # Fill missing values for categorical columns with the mode (most frequent value)
        for col in categorical_cols:
            train_df[col] = train_df[col].fillna(train_df[col].mode()[0])
            test_df[col] = test_df[col].fillna(test_df[col].mode()[0])

        

        # Drop the 'price' column from both train and test data
        train_df = train_df.drop(columns=['price','id'], errors='ignore')  # 'price' is your target variable
        test_df = test_df.drop(columns=['price','id'], errors='ignore')
        
        # One-hot encode categorical features
        train_df_encoded = pd.get_dummies(train_df, drop_first=True)
        test_df_encoded = pd.get_dummies(test_df, drop_first=True)
        
        # Save the columns for later use (to ensure same features during prediction)
        self.columns = train_df_encoded.columns  # Store the columns after encoding
        
        # Recalculate numerical columns after dropping 'price'
        numerical_cols = train_df_encoded.select_dtypes(include=['float64', 'int64']).columns
        
        # Scale the numerical columns
        train_df_encoded[numerical_cols] = self.scaler.fit_transform(train_df_encoded[numerical_cols])
        test_df_encoded[numerical_cols] = self.scaler.transform(test_df_encoded[numerical_cols])
        
        # Save the preprocessor (scaler and encoder) to a file
        self.save_preprocessor()
        
        return train_df_encoded, test_df_encoded
    
    def save_preprocessor(self):
        # Save the scaler and encoder columns as part of the preprocessor.pkl
        joblib.dump({
            'scaler': self.scaler,
            'encoder_columns': self.columns  # Save the column names after encoding
        }, 'artifacts/preprocessor1.pkl')
        print("Preprocessor saved as preprocessor1.pkl")
        print("Columns saved in preprocessor:", self.columns)

    
    def transform_for_prediction(self, input_df: pd.DataFrame, scaler, encoder_columns):
        # Handle missing values and one-hot encoding during prediction
        input_df = input_df.drop(columns=['price','id'], errors='ignore')  # Drop price and id if present
        
        # One-hot encode categorical features
        input_df_encoded = pd.get_dummies(input_df, drop_first=True)
        missing_cols=set(encoder_columns)-set(input_df_encoded.columns)

        for col in missing_cols:
            input_df_encoded[col]=0 
        
        # Re-align columns: Add missing columns with 0s if necessary (to match training set)
        input_df_encoded = input_df_encoded.reindex(columns=encoder_columns, fill_value=0)
        
        # Scale the numerical columns (apply the same scaler)
        numerical_cols = input_df.select_dtypes(include=['float64', 'int64']).columns
        input_df_encoded[numerical_cols] = scaler.transform(input_df_encoded[numerical_cols])
        
        return input_df_encoded
