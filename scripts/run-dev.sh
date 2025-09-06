#!/bin/bash

# 网球分析项目开发环境启动脚本
# 作者: GitHub Copilot

set -e

echo "🎾 启动网球分析开发环境..."

# 检查 X11 转发设置（用于GUI显示）
if [[ -z "$DISPLAY" ]]; then
    echo "⚠️  警告: DISPLAY 环境变量未设置，GUI功能可能无法使用"
    export DISPLAY=:0
fi

# 允许 X11 转发
xhost +local:docker > /dev/null 2>&1 || echo "⚠️  无法设置 X11 转发，GUI 功能可能受限"

# 进入 docker 目录
cd docker

# 启动开发容器
echo "🚀 启动开发容器..."
docker-compose up -d tennis-analysis

# 进入容器的交互式bash
echo "🔧 进入开发环境..."
docker-compose exec tennis-analysis /bin/bash

echo "👋 已退出开发环境"
