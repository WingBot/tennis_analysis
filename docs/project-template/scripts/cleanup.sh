#!/bin/bash

# Cleanup script template
# Customize for your project

set -e

echo "🧹 Cleaning up [YOUR_PROJECT_NAME] environment..."

echo "Stopping containers..."
cd docker
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
cd ..

echo "Removing unused images..."
docker image prune -f

echo "Removing unused volumes..."
docker volume prune -f

echo "Removing unused networks..."
docker network prune -f

echo "✅ Cleanup completed!"
echo ""
echo "📊 Current Docker usage:"
docker system df