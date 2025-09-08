#!/bin/bash

# Interactive management script template
# Customize for your project

echo "🚀 [YOUR_PROJECT_NAME] - Management Interface"
echo "=============================================="

# Display menu
echo ""
echo "🏗️  Build Stage:"
echo "1) Build base image (fast, system deps only)"
echo "2) Start development environment"
echo "3) Install and test dependencies"
echo "4) Generate final production image"
echo ""
echo "🚀 Usage Stage:"
echo "5) Run main application"
echo "6) Start Jupyter Lab"
echo ""
echo "🧹 Maintenance:"
echo "7) Cleanup environment"
echo "8) View image status"
echo "0) Exit"

read -p "Enter option (0-8): " choice

case $choice in
    1)
        echo "🔨 Building base image..."
        ./scripts/build-base.sh
        ;;
    2)
        echo "🔧 Starting development environment..."
        ./scripts/run-dev.sh
        ;;
    3)
        echo "📦 Please run in development container:"
        echo "   ./scripts/install-deps.sh"
        echo "   ./scripts/test-env.sh"
        echo ""
        echo "After validation, proceed to option 4"
        ;;
    4)
        echo "🎯 Generating final production image..."
        echo "This feature needs to be implemented for your project"
        # ./scripts/build-final.sh
        ;;
    5)
        echo "🎯 Running main application..."
        echo "Customize this section for your application"
        # docker run -it your-project:latest
        ;;
    6)
        echo "📚 Starting Jupyter Lab..."
        cd docker
        docker-compose -f docker-compose.dev.yml up -d your-project-jupyter
        echo "🌐 Access at http://localhost:8888"
        ;;
    7)
        echo "🧹 Cleaning up environment..."
        docker system prune -f
        echo "✅ Cleanup completed"
        ;;
    8)
        echo "📊 Checking image status..."
        echo "Base image:"
        docker images | grep your-project-base || echo "  Not built"
        echo "Production image:"
        docker images | grep "your-project.*latest" || echo "  Not built"
        echo "Running containers:"
        docker ps | grep your-project || echo "  None"
        ;;
    0)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid option, please run script again"
        exit 1
        ;;
esac