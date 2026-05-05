# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Flask (required for the app to run)
RUN pip install --no-cache-dir flask

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
