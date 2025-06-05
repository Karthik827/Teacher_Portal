# Use Python 3.9 as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn

# Copy project
COPY . .

# Create static directory and collect static files
RUN mkdir -p static && python manage.py collectstatic --noinput

# Run uvicorn instead of gunicorn
CMD uvicorn Teacher_portal.asgi:application --host 0.0.0.0 --port $PORT

