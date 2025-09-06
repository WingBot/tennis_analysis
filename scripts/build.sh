#!/bin/bash

# 网球分析项目 Docker 构建脚本
# 作者: GitHub Copilot
# 日期: $(date)

set -e

echo "🎾 开始构建网球分析项目 Docker 镜像..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 检查 Docker 服务是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 服务未运行，请启动 Docker 服务"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p input_videos output_videos models runs/detect tracker_stubs logs

# 进入 docker 目录
cd docker

# 构建 Docker 镜像
echo "🔨 构建 Docker 镜像..."
docker-compose build --no-cache

# 返回项目根目录
cd ..

echo "✅ Docker 镜像构建完成！"

# 显示镜像信息
echo "📊 Docker 镜像信息："
docker images | grep tennis

echo ""
echo "🚀 使用以下命令启动项目："
echo "   开发模式:     ./scripts/run-dev.sh"
echo "   运行主程序:   ./scripts/run-main.sh"
echo "   启动Jupyter:  ./scripts/run-notebook.sh"
echo "   训练模式:     ./scripts/run-training.sh"
