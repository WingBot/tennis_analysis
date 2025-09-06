#!/bin/bash

# Jupyter Notebook 启动脚本
# 作者: GitHub Copilot

set -e

echo "📚 启动 Jupyter Notebook 服务..."

# 进入 docker 目录
cd docker

# 启动 Jupyter 服务
echo "🚀 启动 Jupyter 容器..."
docker-compose up -d tennis-notebook

# 等待服务启动
echo "⏳ 等待 Jupyter 服务启动..."
sleep 5

# 显示访问地址
echo "✅ Jupyter Lab 已启动！"
echo ""
echo "🌐 访问地址: http://localhost:8888"
echo ""
echo "📁 可用的 Notebook："
echo "   - analysis/ball_analysis.ipynb"
echo "   - training/tennis_ball_detector_training.ipynb"
echo "   - training/tennis_court_keypoints_training.ipynb"
echo ""
echo "🛑 停止服务: docker-compose down"
echo "📋 查看日志: docker-compose logs tennis-notebook"
