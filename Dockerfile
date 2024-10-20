FROM python:3.9

# Install necessary libraries
RUN pip install xgboost pymongo pandas scikit-learn

# Copy the training script to the container
COPY train.py /train.py

# Set the entry point to run the training script
CMD ["python", "/train.py"]
