#!/bin/bash

# 验证依赖安装和功能测试脚本
# 作者: GitHub Copilot

set -e

echo "🧪 开始验证开发环境..."

# 测试 Python 基础功能
echo "🐍 测试 Python 基础功能..."
python3 -c "
import sys
print(f'Python 版本: {sys.version}')
print(f'Python 路径: {sys.executable}')
"

# 测试核心依赖
echo "📦 测试核心依赖..."
python3 -c "
import numpy as np
print(f'✅ NumPy {np.__version__} - 正常')

import cv2
print(f'✅ OpenCV {cv2.__version__} - 正常')

from PIL import Image
print(f'✅ Pillow - 正常')

import matplotlib
print(f'✅ Matplotlib {matplotlib.__version__} - 正常')
"

# 测试机器学习依赖
echo "🤖 测试机器学习依赖..."
python3 -c "
try:
    import torch
    print(f'✅ PyTorch {torch.__version__} - 正常')
    print(f'   CUDA 可用: {torch.cuda.is_available()}')
except ImportError as e:
    print(f'❌ PyTorch 导入失败: {e}')

try:
    import torchvision
    print(f'✅ TorchVision {torchvision.__version__} - 正常')
except ImportError as e:
    print(f'❌ TorchVision 导入失败: {e}')

try:
    import ultralytics
    print(f'✅ Ultralytics - 正常')
except ImportError as e:
    print(f'❌ Ultralytics 导入失败: {e}')
"

# 测试数据处理依赖
echo "📊 测试数据处理依赖..."
python3 -c "
try:
    import pandas as pd
    print(f'✅ Pandas {pd.__version__} - 正常')
except ImportError as e:
    print(f'❌ Pandas 导入失败: {e}')

try:
    import sklearn
    print(f'✅ Scikit-learn {sklearn.__version__} - 正常')
except ImportError as e:
    print(f'❌ Scikit-learn 导入失败: {e}')
"

# 测试项目模块
echo "🎾 测试项目模块..."
if [[ -f "main.py" ]]; then
    python3 -c "
try:
    from utils import read_video, save_video
    print('✅ 项目 utils 模块 - 正常')
except ImportError as e:
    print(f'❌ 项目 utils 模块导入失败: {e}')

try:
    from trackers import PlayerTracker, BallTracker
    print('✅ 项目 trackers 模块 - 正常')
except ImportError as e:
    print(f'❌ 项目 trackers 模块导入失败: {e}')

try:
    from court_line_detector import CourtLineDetector
    print('✅ 项目 court_line_detector 模块 - 正常')
except ImportError as e:
    print(f'❌ 项目 court_line_detector 模块导入失败: {e}')
"
else
    echo "⚠️  main.py 文件不存在，跳过项目模块测试"
fi

echo ""
echo "📋 已安装包列表："
pip list | head -20

echo ""
echo "💾 磁盘使用情况："
df -h /

echo ""
echo "🎯 验证完成！如果看到 ✅ 表示该模块工作正常"
echo "   如果看到 ❌ 表示需要进一步安装或调试"
