# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY train.py .
COPY .env .

# Create directory for model storage
RUN mkdir -p /mnt/block_storage

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Command to run the training script
CMD ["python", "train.py"]