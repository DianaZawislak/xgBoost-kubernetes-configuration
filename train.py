from pymongo import MongoClient
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

# MongoDB connection
client = MongoClient('mongodb://monitoringUser:XZ536Qm9XRxs@10.108.0.15:27017')
db = client['rentals']  # Connecting to 'rentals' database
collection = db['zip_33131']  # Using the 'zip_33131' collection

# Data extraction with query (example: extracting data for 2023 and beyond)
query = {"data.Listing_date": {"$gte": "2023-01-01"}}  # Example query
data = list(collection.find(query))
df = pd.DataFrame(data)

# Preprocessing the data
# Ensure fields like 'beds', 'baths', 'sqft', and 'rent_amount' are properly formatted
if 'beds' in df.columns:
    df['beds'] = pd.to_numeric(df['beds'], errors='coerce').fillna(0)
else:
    print("Column 'beds' does not exist in the data")

if 'baths' in df.columns:
    df['baths'] = pd.to_numeric(df['baths'], errors='coerce').fillna(0)
else:
    print("Column 'baths' does not exist in the data")

if 'sqft' in df.columns:
    df['sqft'] = pd.to_numeric(df['sqft'], errors='coerce').fillna(0)
else:
    print("Column 'sqft' does not exist in the data")

# Extract and clean 'rent_amount'
df['rent_amount'] = df['data'].apply(
    lambda x: float(x['rent_amount'].replace('$', '').replace(',', '')) if 'rent_amount' in x else None
).fillna(0)

# Extract 'Listing_date' to create 'month' and 'year' features
df['Listing_date'] = pd.to_datetime(df['data'].apply(
    lambda x: x['Listing_date'] if 'Listing_date' in x else None
), errors='coerce')

df['month'] = df['Listing_date'].dt.month.fillna(0).astype(int)
df['year'] = df['Listing_date'].dt.year.fillna(0).astype(int)

# Features and target
X = df[['beds', 'baths', 'sqft', 'month', 'year']]
y = df['rent_amount']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost model training
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000, learning_rate=0.05, max_depth=6, random_state=42)
model.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_test, y_test)], verbose=True)

# Save the trained model
model.save_model('/mnt/block_storage/xgboost_model.bin')
