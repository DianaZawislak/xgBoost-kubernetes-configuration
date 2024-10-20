from pymongo import MongoClient
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

# MongoDB connection
client = MongoClient('mongodb://monitoringUser:XZ536Qm9XRxs@159.65.167.68:27017')
db = client['your_database']
collection = db['your_collection']

# Data extraction
query = {"Listing_date": {"$gte": "2023-01-01"}}  # Example query for the last 12 months
data = list(collection.find(query))
df = pd.DataFrame(data)

# Preprocessing
df['beds'] = df['beds'].astype(float)
df['baths'] = df['baths'].astype(float)
df['sqft'] = df['sqft'].replace(',', '', regex=True).astype(float)
df['rent_amount'] = df['rent_amount'].replace({'\$': '', ',': ''}, regex=True).astype(float)

df['month'] = pd.to_datetime(df['Listing_date']).dt.month
df['year'] = pd.to_datetime(df['Listing_date']).dt.year
X = df[['beds', 'baths', 'sqft', 'month', 'year']]
y = df['rent_amount']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost model training
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000, learning_rate=0.05, max_depth=6, random_state=42)
model.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_test, y_test)], verbose=True)

# Save the trained model
model.save_model('/mnt/block_storage/xgboost_model.bin')
