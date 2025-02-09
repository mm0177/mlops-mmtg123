import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def ModelTrainer(X_train, y_train, X_valid, y_valid, model_output_path):
    # Initialize the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_valid)
    
    # Evaluate the model
    mse = mean_squared_error(y_valid, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_valid, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {rmse}")
    print(f"R-squared: {r2}")
    
    # Save the trained model to disk
    joblib.dump(model, model_output_path)
    
    return model, mse, rmse, r2

# Example usage
if __name__ == "__main__":
   
    df = pd.read_csv('./artifacts/train.csv')
    X = df.drop(columns=['price'])
    y = df['price']
    
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
    
    ModelTrainer(X_train, y_train, X_valid, y_valid, './artifacts/random_forest_model.pkl')
