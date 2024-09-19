# Use an official Python runtime as a parent image
FROM python:3.11-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get clean \
# Create workdir and copy files
RUN mkdir app
COPY /backend/. /app/
# Set the working directory
WORKDIR /app
# Install MongoDB client for Djongo
#RUN apt-get update && apt-get install -y \
#    mongodb-clients \
#    && apt-get clean
# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt  # Saves space preventing package cacheing
# Expose port 8000 for the Django application
EXPOSE 8000
# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
