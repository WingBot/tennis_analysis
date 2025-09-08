#!/bin/bash

# Environment validation script template
# Customize for your project

set -e

echo "🧪 Validating [YOUR_PROJECT_NAME] environment..."

# Test Python basics
echo "🐍 Testing Python basics..."
python3 -c "
import sys
print(f'Python version: {sys.version}')
print(f'Python executable: {sys.executable}')
"

# Test core dependencies
echo "📦 Testing core dependencies..."
python3 -c "
try:
    import numpy as np
    print(f'✅ NumPy {np.__version__} - OK')
except ImportError as e:
    print(f'❌ NumPy failed: {e}')

# Add your core dependency tests here
# try:
#     import pandas as pd
#     print(f'✅ Pandas {pd.__version__} - OK')
# except ImportError as e:
#     print(f'❌ Pandas failed: {e}')
"

# Test ML dependencies (customize/remove as needed)
echo "🤖 Testing ML dependencies..."
python3 -c "
try:
    import torch
    print(f'✅ PyTorch {torch.__version__} - OK')
    print(f'   CUDA available: {torch.cuda.is_available()}')
except ImportError as e:
    print(f'❌ PyTorch failed: {e}')

# Add your ML framework tests here
"

# Test project modules
echo "🎯 Testing project modules..."
if [[ -f "main.py" ]]; then
    python3 -c "
# Add your project-specific module tests here
# try:
#     from your_module import YourClass
#     print('✅ Your module - OK')
# except ImportError as e:
#     print(f'❌ Your module failed: {e}')
print('✅ Project structure - OK')
"
else
    echo "⚠️  main.py not found, skipping project module tests"
fi

echo ""
echo "📋 Installed packages (top 20):"
pip list | head -20

echo ""
echo "💾 Disk usage:"
df -h /

echo ""
echo "🎯 Validation completed! ✅ means OK, ❌ means needs attention"