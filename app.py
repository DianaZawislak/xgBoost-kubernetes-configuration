from flask import Flask, request, jsonify
import xgboost as xgb
import pandas as pd

app = Flask(__name__)

# Load the trained model from the persistent volume
model = xgb.XGBRegressor()
model.load_model('/mnt/block_storage/xgboost_model.bin')

@app.route('/predict', methods=['POST'])
def predict():
    # Expect JSON input with feature data for the model
    data = request.json
    df = pd.DataFrame([data])

    # Make a prediction using the XGBoost model
    prediction = model.predict(df)

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
