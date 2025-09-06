#!/bin/bash

# 从开发环境生成最终生产镜像脚本
# 作者: GitHub Copilot

set -e

echo "🎯 从开发环境生成最终生产镜像..."

# 检查开发容器是否在运行
if ! docker ps | grep -q tennis-dev; then
    echo "❌ 开发容器未运行，请先启动: ./scripts/run-dev-base.sh"
    exit 1
fi

# 获取容器中已安装的包列表
echo "📦 获取已安装的包列表..."
docker exec tennis-dev pip freeze > requirements-final.txt

echo "📋 生成的最终依赖列表："
cat requirements-final.txt

# 创建最终的 Dockerfile
echo "🔨 创建最终生产 Dockerfile..."
cat > docker/Dockerfile.final << 'EOF'
# 最终生产镜像 - 包含所有验证过的依赖
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libjpeg-dev \
    libpng-dev \
    build-essential \
    pkg-config \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 复制最终的依赖文件
COPY requirements-final.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-final.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p input_videos output_videos models runs/detect tracker_stubs logs

# 设置权限
RUN find scripts -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true

# 创建非 root 用户
RUN useradd -m -u 1000 tennis && \
    chown -R tennis:tennis /app
USER tennis

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import cv2, torch, ultralytics; print('OK')" || exit 1

# 暴露端口
EXPOSE 8888

# 默认启动命令
CMD ["python", "main.py"]
EOF

# 构建最终镜像
echo "🚀 构建最终生产镜像..."
cd docker
docker build -f Dockerfile.final -t tennis-analysis:latest ..
cd ..

if [[ $? -eq 0 ]]; then
    echo "✅ 最终镜像构建成功！"
    
    # 显示镜像信息
    echo "📊 最终镜像信息："
    docker images | grep tennis-analysis
    
    # 清理开发容器
    read -p "是否清理开发环境容器？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd docker
        docker-compose -f docker-compose.dev.yml down
        cd ..
        echo "🧹 开发环境已清理"
    fi
    
    echo ""
    echo "🎉 生产镜像准备完成！"
    echo "使用 docker run -it tennis-analysis:latest 运行"
else
    echo "❌ 最终镜像构建失败"
    exit 1
fi
