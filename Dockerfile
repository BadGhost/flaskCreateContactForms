# Use the official Python image as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port on which the application will run
EXPOSE 80

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
