#!/bin/bash

# 网球分析项目清理脚本
# 作者: GitHub Copilot

set -e

echo "🧹 清理网球分析项目环境..."

# 进入 docker 目录
cd docker

# 停止所有容器
echo "🛑 停止所有相关容器..."
docker-compose down

# 返回项目根目录
cd ..

# 清理容器
echo "🗑️  删除容器..."
docker container prune -f

# 选择性清理镜像（询问用户）
read -p "是否删除 Docker 镜像？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  删除 Docker 镜像..."
    docker images | grep tennis | awk '{print $3}' | xargs -r docker rmi -f
fi

# 清理生成的文件（询问用户）
read -p "是否清理输出文件？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  清理输出文件..."
    rm -rf output_videos/*
    rm -rf runs/detect/*
    rm -rf logs/*
    echo "✅ 输出文件已清理"
fi

echo "✅ 清理完成！"
