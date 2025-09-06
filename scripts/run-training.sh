#!/bin/bash

# 网球分析训练环境启动脚本
# 作者: GitHub Copilot

set -e

echo "🏋️ 启动网球分析训练环境..."

# 检查 GPU 是否可用
if command -v nvidia-smi &> /dev/null; then
    echo "🚀 检测到 NVIDIA GPU"
    nvidia-smi
else
    echo "⚠️  未检测到 GPU，将使用 CPU 训练（速度较慢）"
fi

# 进入 docker 目录
cd docker

# 启动训练容器
echo "🚀 启动训练容器..."
docker-compose up -d tennis-training

# 进入容器的交互式bash
echo "🔧 进入训练环境..."
docker-compose exec tennis-training /bin/bash

echo "👋 已退出训练环境"
