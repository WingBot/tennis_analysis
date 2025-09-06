#!/bin/bash

# 启动基础开发环境脚本
# 作者: GitHub Copilot

set -e

echo "🎾 启动基础开发环境..."

# 检查 X11 转发
if [[ -z "$DISPLAY" ]]; then
    echo "⚠️  设置默认 DISPLAY"
    export DISPLAY=:0
fi

# 允许 X11 转发
xhost +local:docker > /dev/null 2>&1 || echo "⚠️  无法设置 X11 转发"

# 进入 docker 目录
cd docker

# 启动基础开发容器
echo "🚀 启动基础开发容器..."
docker-compose -f docker-compose.dev.yml up -d tennis-dev

# 等待容器启动
sleep 2

echo ""
echo "🔧 进入开发环境..."
echo "在容器内执行以下命令安装依赖："
echo "  ./scripts/install-deps.sh"
echo ""

# 进入容器
docker-compose -f docker-compose.dev.yml exec tennis-dev /bin/bash

echo "👋 已退出开发环境"
