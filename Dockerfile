# Use the official Python image as a base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to the Docker container
COPY ./celery_django_sample /app/

# Run Django server
CMD ["celery", "--app", "celery_django_sample", "worker", "--concurrency", "2", "--pool=threads", "--loglevel=info"]
