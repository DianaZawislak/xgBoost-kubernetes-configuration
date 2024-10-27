from pymongo import MongoClient
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import os
import sys
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import json

print("Starting training script...")

# MongoDB credentials
username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')

# MongoDB connection parameters
host = "10.108.0.15"  # MongoDB IP
port = "27017"        # MongoDB port
database = "rentals"  # Target database
collection_name = "zip_33131"  # Target collection

# Construct MongoDB URI with authSource=admin
mongo_uri = f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"

try:
    print("Connecting to MongoDB...")
    print(f"Connection string (without password): {mongo_uri.replace(password, '****')}")
    
    # Create MongoDB client
    client = MongoClient(mongo_uri)
    
    # Test connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
    
    # Access the specific database and collection
    db = client[database]
    collection = db[collection_name]
    
    # Fetch data
    print("Fetching data...")
    data = list(collection.find({}))
    print(f"Retrieved {len(data)} documents")
    
    if len(data) == 0:
        raise Exception("No data found in collection")

    # Convert to DataFrame
    print("Converting to DataFrame...")
    df = pd.DataFrame(data)
    print(f"DataFrame shape: {df.shape}")
    
    # Debugging information
    print("\nAvailable columns:", df.columns.tolist())
    print("\nSample document:", data[0] if data else "No data")

    # Process fields
    df['beds'] = pd.to_numeric(df['beds'], errors='coerce').fillna(0)
    df['baths'] = pd.to_numeric(df['baths'], errors='coerce').fillna(0)
    df['sqft'] = pd.to_numeric(df['sqft'], errors='coerce').fillna(0)
    df['rent_amount'] = pd.to_numeric(df['rent_amount'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce').fillna(0)
    
    # Process nested data fields
    df['lat'] = df['data'].apply(lambda x: float(x.get('lat', 0)) if isinstance(x, dict) else 0)
    df['lng'] = df['data'].apply(lambda x: float(x.get('lng', 0)) if isinstance(x, dict) else 0)
    
    df['listing_date'] = pd.to_datetime(
        df['data'].apply(lambda x: x.get('Listing_date') if isinstance(x, dict) else None),
        errors='coerce'
    )
    
    # Create time features
    df['month'] = df['listing_date'].dt.month.fillna(0).astype(int)
    df['year'] = df['listing_date'].dt.year.fillna(0).astype(int)
    
    # Feature selection
    features = ['beds', 'baths', 'sqft', 'month', 'year', 'lat', 'lng']
    X = df[features]
    y = df['rent_amount']
    
    print("\nFeature statistics:")
    print(X.describe())
    print("\nTarget statistics:")
    print(y.describe())
    
    # Handle any missing values
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)
    
    # Train-test split
    print("\nSplitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train model
    print("\nTraining XGBoost model...")
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
    
    model.fit(
        X_train,
        y_train,
        early_stopping_rounds=10,
        eval_set=[(X_test, y_test)],
        verbose=True
    )
    
    # Model evaluation
    print("\nEvaluating model performance...")
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, train_predictions))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))
    train_r2 = r2_score(y_train, train_predictions)
    test_r2 = r2_score(y_test, test_predictions)
    
    print(f"\nModel Performance Metrics:")
    print(f"Training RMSE: ${train_rmse:,.2f}")
    print(f"Test RMSE: ${test_rmse:,.2f}")
    print(f"Training R² Score: {train_r2:.4f}")
    print(f"Test R² Score: {test_r2:.4f}")
    
    # Feature importance
    importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    })
    importance = importance.sort_values('importance', ascending=False)
    print("\nFeature Importance:")
    print(importance)
    
    # Save model and feature information
    print("\nSaving model and feature information...")
    model.save_model('/mnt/block_storage/xgboost_model.bin')
    
    # Save feature information for API use
    feature_info = {
        'features': features,
        'feature_importance': importance.to_dict('records'),
        'model_metrics': {
            'train_rmse': float(train_rmse),
            'test_rmse': float(test_rmse),
            'train_r2': float(train_r2),
            'test_r2': float(test_r2)
        }
    }
    
    with open('/mnt/block_storage/model_info.json', 'w') as f:
        json.dump(feature_info, f, indent=2)
    
    print("Training completed successfully!")

except Exception as e:
    print(f"ERROR: {str(e)}")
    print("\nTraceback:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
