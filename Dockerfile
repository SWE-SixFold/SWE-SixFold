# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the entire app directory into the container
COPY . /app/app

# Install dependencies from requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set environment variable for Google credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json

# Expose the port that Flask will run on
EXPOSE 8080

# Run the Flask app
CMD ["python", "/app/app.py"]  # Ensure the path points to /app/app.py
