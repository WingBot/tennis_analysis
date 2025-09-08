# Simple all-in-one Dockerfile template
# For quick setup and testing - customize as needed
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies (customize as needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-base.txt .
RUN pip install --no-cache-dir -r requirements-base.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data output models logs

# Set permissions for scripts
RUN find scripts -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true

# Expose port (customize as needed)
EXPOSE 8888

# Set environment variables
ENV PYTHONPATH=/app

# Default command (customize for your main application)
CMD ["python", "main.py"]