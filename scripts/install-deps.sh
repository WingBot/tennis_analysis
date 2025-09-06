#!/bin/bash

# 分阶段安装 Python 依赖
# 作者: GitHub Copilot

set -e

echo "🔧 开始分阶段安装 Python 依赖..."

# 第一阶段：基础依赖
echo "📦 第一阶段：安装基础依赖..."
if pip install -r requirements-base.txt; then
    echo "✅ 基础依赖安装成功"
else
    echo "❌ 基础依赖安装失败"
    exit 1
fi

# 第二阶段：机器学习依赖
echo "🤖 第二阶段：安装机器学习依赖..."
if pip install -r requirements-ml.txt; then
    echo "✅ 机器学习依赖安装成功"
else
    echo "❌ 机器学习依赖安装失败，但继续安装其他依赖"
fi

# 第三阶段：数据处理依赖
echo "📊 第三阶段：安装数据处理依赖..."
if pip install -r requirements-data.txt; then
    echo "✅ 数据处理依赖安装成功"
else
    echo "❌ 数据处理依赖安装失败，但继续安装其他依赖"
fi

# 第四阶段：开发工具依赖
echo "🛠️ 第四阶段：安装开发工具依赖..."
if pip install -r requirements-dev.txt; then
    echo "✅ 开发工具依赖安装成功"
else
    echo "❌ 开发工具依赖安装失败，但不影响核心功能"
fi

echo ""
echo "📋 安装完成的包列表："
pip list

echo ""
echo "🎯 核心功能测试："
python -c "
try:
    import cv2
    print('✅ OpenCV 可用')
except ImportError:
    print('❌ OpenCV 不可用')

try:
    import numpy
    print('✅ NumPy 可用')
except ImportError:
    print('❌ NumPy 不可用')

try:
    import torch
    print('✅ PyTorch 可用')
except ImportError:
    print('❌ PyTorch 不可用')

try:
    import ultralytics
    print('✅ YOLO 可用')
except ImportError:
    print('❌ YOLO 不可用')
"

echo "✅ 依赖安装过程完成！"
