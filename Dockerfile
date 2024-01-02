# Use an official Python runtime as a parent image
# Use bullseye image for raspberry pi /arm64/v8
FROM python:3.9.18-slim-bullseye  

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "-m", "app.main"]

