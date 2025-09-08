#!/bin/bash

# Build base Docker image template
# Customize this script for your project

set -e

echo "🔨 Building base image for [YOUR_PROJECT_NAME]..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker service not running, please start Docker"
    exit 1
fi

# Build base image
echo "🔨 Building base image (system dependencies only)..."
cd docker
docker build -f Dockerfile.base -t your-project-base:latest ..
cd ..

if [[ $? -eq 0 ]]; then
    echo "✅ Base image built successfully!"
    
    # Show image info
    echo "📊 Base image info:"
    docker images | grep your-project-base
    
    echo ""
    echo "🚀 Next steps:"
    echo "1. Start development environment: ./scripts/run-dev.sh"
    echo "2. Install dependencies in container: ./scripts/install-deps.sh"
    echo "3. Test functionality, then build final image"
else
    echo "❌ Base image build failed"
    exit 1
fi