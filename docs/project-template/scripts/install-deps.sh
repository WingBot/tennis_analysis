#!/bin/bash

# Staged dependency installation template
# Customize for your project

set -e

echo "🔧 Installing [YOUR_PROJECT_NAME] dependencies..."

# Stage 1: Base dependencies
echo "📦 Stage 1: Installing base dependencies..."
if pip install -r requirements-base.txt; then
    echo "✅ Base dependencies installed successfully"
else
    echo "❌ Base dependencies failed"
    exit 1
fi

# Stage 2: ML dependencies (remove if not needed)
echo "🤖 Stage 2: Installing ML dependencies..."
if pip install -r requirements-ml.txt; then
    echo "✅ ML dependencies installed successfully"
else
    echo "❌ ML dependencies failed, continuing..."
fi

# Stage 3: Development dependencies
echo "🛠️ Stage 3: Installing development dependencies..."
if pip install -r requirements-dev.txt; then
    echo "✅ Development dependencies installed successfully"
else
    echo "❌ Development dependencies failed, but core functions should work"
fi

echo ""
echo "📋 Installed packages:"
pip list

echo ""
echo "🎯 Core functionality test:"
python -c "
try:
    import numpy
    print('✅ NumPy available')
except ImportError:
    print('❌ NumPy not available')

# Add your core imports here
# try:
#     import your_core_module
#     print('✅ Core module available')
# except ImportError:
#     print('❌ Core module not available')
"

echo "✅ Dependency installation completed!"