#!/bin/bash

# 构建基础 Docker 镜像脚本
# 作者: GitHub Copilot

set -e

echo "🎾 构建网球分析基础镜像..."

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 服务未运行，请启动 Docker 服务"
    exit 1
fi

# 进入 docker 目录
cd docker

# 构建基础镜像
echo "🔨 构建基础镜像（不包含 Python 依赖）..."
docker build -f Dockerfile.base -t tennis-analysis-base:latest ..

if [[ $? -eq 0 ]]; then
    echo "✅ 基础镜像构建成功！"
    
    # 显示镜像信息
    echo "📊 基础镜像信息："
    docker images | grep tennis-analysis-base
    
    echo ""
    echo "🚀 下一步："
    echo "1. 启动开发环境: ./scripts/run-dev-base.sh"
    echo "2. 在容器内安装依赖: ./scripts/install-deps.sh"
    echo "3. 测试功能后再构建完整镜像"
else
    echo "❌ 基础镜像构建失败"
    exit 1
fi
