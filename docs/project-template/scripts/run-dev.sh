#!/bin/bash

# Development environment startup script template
# Customize for your project

set -e

echo "🚀 Starting [YOUR_PROJECT_NAME] development environment..."

# Check X11 forwarding setup (for GUI apps - remove if not needed)
if [[ -z "$DISPLAY" ]]; then
    echo "⚠️  Warning: DISPLAY not set, GUI features may not work"
    export DISPLAY=:0
fi

# Allow X11 forwarding (remove if not needed)
xhost +local:docker > /dev/null 2>&1 || echo "⚠️  Cannot set X11 forwarding"

# Enter docker directory
cd docker

# Start development container
echo "🚀 Starting development container..."
docker-compose -f docker-compose.dev.yml up -d your-project-dev

# Enter interactive bash
echo "🔧 Entering development environment..."
docker-compose -f docker-compose.dev.yml exec your-project-dev /bin/bash

echo "👋 Exited development environment"