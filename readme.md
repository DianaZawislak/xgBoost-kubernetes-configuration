# XGBoost Property Price Prediction - Kubernetes Deployment

## Project Overview
This project implements a machine learning system for real estate price prediction using XGBoost, deployed on a DigitalOcean Kubernetes cluster. The system consists of two main components:
1. A training pipeline that processes historical rental data from MongoDB
2. An API service that serves predictions in real-time

## Architecture
```
                                   ┌─────────────────┐
                                   │   MongoDB       │
                                   │  (External DB)  │
                                   └────────┬────────┘
                                           │
                                           ▼
┌─────────────────┐              ┌─────────────────┐
│                 │              │                 │
│  Training Job   ├──────────────▶  Persistent    │
│   (XGBoost)     │              │   Volume       │
│                 │              │                 │
└─────────────────┘              └────────┬────────┘
                                         │
                                         ▼
┌─────────────────┐              ┌─────────────────┐
│    API          │              │                 │
│   Service       │◄─────────────┤  Model Storage  │
│  (Flask)        │              │                 │
└─────────────────┘              └─────────────────┘
```

## Components

### 1. Training Pipeline
- Fetches rental data from MongoDB
- Processes and cleans the data
- Trains XGBoost model
- Saves model to persistent storage

### 2. API Service
- Loads trained model from persistent storage
- Provides REST endpoints for predictions
- Handles real-time inference requests

### 3. Infrastructure
- DigitalOcean Kubernetes Cluster
- Persistent Volume Claims for model storage
- MongoDB for data storage
- Kubernetes Services for networking

## Project Structure
```
xgBoost-kubernetes-configuration/
├── Dockerfile                  # Training container configuration
├── Dockerfile.api             # API container configuration
├── app.py                    # Flask API application
├── train.py                 # Training script
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore rules
└── kubernetes/
    ├── mongodb-service.yaml        # MongoDB service configuration
    ├── mongo-secret.template.yaml  # Template for MongoDB credentials
    ├── mongo-secret.yaml          # MongoDB credentials (not in git)
    ├── xgboost-model-pvc.yaml     # Persistent volume claim
    ├── xgboost-training-job.yaml  # Training job configuration
    └── xgboost-api-deployment.yaml # API deployment configuration
```

## Prerequisites
- DigitalOcean account
- `kubectl` configured for your cluster
- Docker installed
- MongoDB instance running

## Environment Variables
Required environment variables (stored in `.env` and Kubernetes secrets):
```
MONGO_USERNAME=<username>
MONGO_PASSWORD=<password>
MONGO_HOST=<host>
MONGO_PORT=<port>
MONGO_DATABASE=<database>
MONGO_COLLECTION=<collection>
```

## Deployment Instructions

1. Configure MongoDB Access
```bash
# Create MongoDB credentials secret
kubectl apply -f mongo-secret.yaml
```

2. Set Up Storage
```bash
# Create persistent volume claim
kubectl apply -f xgboost-model-pvc.yaml
```

3. Deploy MongoDB Service
```bash
# Create MongoDB service
kubectl apply -f mongodb-service.yaml
```

4. Run Training Job
```bash
# Deploy training job
kubectl apply -f xgboost-training-job.yaml
```

5. Deploy API Service
```bash
# Deploy API
kubectl apply -f xgboost-api-deployment.yaml
```

## API Endpoints

### Prediction Endpoint
```
POST /predict
Content-Type: application/json

{
    "beds": 2,
    "baths": 2,
    "sqft": 1000,
    "month": 1,
    "year": 2024
}
```

## Monitoring and Maintenance

### Check Status
```bash
# View all resources
kubectl get all -n xgboost-service

# Check logs
kubectl logs -f <pod-name> -n xgboost-service
```

### Troubleshooting
Common issues and solutions:
1. MongoDB Connection Issues
   - Verify MongoDB service is running
   - Check credentials in secret
   - Verify network connectivity

2. Model Loading Issues
   - Check if training job completed successfully
   - Verify PVC is properly mounted
   - Check model file permissions

## Security Notes
- MongoDB credentials are stored in Kubernetes secrets
- API service runs with read-only access to model storage
- External access is controlled through DigitalOcean firewall rules

## Development
To run locally:
1. Set up virtual environment
2. Install requirements
3. Configure environment variables
4. Run Flask application

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
