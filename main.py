from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://mmeyyappan26:Mkarthik123@mlops.2ajxl.mongodb.net/")
db = client["mlops_db"]
collection = db["experiment_tracking"]

# Insert experiment data
experiment = {
    "model_name": "RandomForest",
    "hyperparameters": {"n_estimators": 100, "max_depth": 10},
    "metrics": {"accuracy": 0.85, "f1_score": 0.78},
    "run_date": "2024-12-17"
}
result = collection.insert_one(experiment)
print(f"Experiment saved with ID: {result.inserted_id}")
