# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend directory, including the pre-generated ChromaDB, into the container
# This assumes you have run the ingest_data.py script locally first
COPY ./backend /app/backend

# Copy the data directory (containing the PDF)
COPY ./data /app/data

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your application
# The host 0.0.0.0 is crucial for the container to be accessible from the outside
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]