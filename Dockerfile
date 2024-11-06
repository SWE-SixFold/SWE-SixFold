# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside the container
EXPOSE 8080

# Define environment variable for Flask
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.app:app"]
