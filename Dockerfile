# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script into the container at /usr/src/app
COPY main.py ./

# Install pytube
# RUN pip install --no-cache-dir pytube
RUN pip install --no-cache-dir pytube youtube-transcript-api fastapi uvicorn

# Run download_captions.py when the container launches
# CMD ["python", "./main.py"]

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

