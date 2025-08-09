# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend directory into the container
COPY ./backend /app/backend

# Copy the data directory (containing the PDF)
COPY ./data /app/data

# ***** FIX: Change the working directory to where the app lives *****
WORKDIR /app/backend

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your application (now simpler)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]