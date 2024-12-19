# Use the official Google Cloud Python base image
FROM gcr.io/google-appengine/python

# Install additional dependencies (dbus and cmake)
RUN apt-get update && \
    apt-get install -y \
    dbus \
    cmake

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . /app/

# Expose the port that the app will run on (default for Flask is 8080)
EXPOSE 8080

# Specify the command to run your application
CMD ["python", "main.py"]  # Replace with the entry point for your app
