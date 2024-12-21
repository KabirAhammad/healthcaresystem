# Use the official Python image as the base image
FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    cmake \
    libdbus-1-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce the image size

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port the app will run on
EXPOSE 8080

# Set the entry point for the app
CMD ["gunicorn", "-b", ":8080", "app:app"]
