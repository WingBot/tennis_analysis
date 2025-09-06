#!/bin/bash

# 网球分析主程序运行脚本
# 作者: GitHub Copilot

set -e

echo "🎾 运行网球分析主程序..."

# 检查输入视频文件是否存在
if [[ ! -f "input_videos/input_video.mp4" ]]; then
    echo "❌ 输入视频文件 'input_videos/input_video.mp4' 不存在"
    echo "请将您的视频文件放置在 input_videos/ 目录下，并命名为 input_video.mp4"
    exit 1
fi

# 检查模型文件
echo "🔍 检查必要的模型文件..."
if [[ ! -f "models/yolo5_last.pt" ]]; then
    echo "⚠️  警告: 球检测模型 'models/yolo5_last.pt' 不存在"
    echo "请下载或训练球检测模型并放置在 models/ 目录下"
fi

if [[ ! -f "models/keypoints_model.pth" ]]; then
    echo "⚠️  警告: 关键点检测模型 'models/keypoints_model.pth' 不存在"
    echo "请下载或训练关键点检测模型并放置在 models/ 目录下"
fi

# 进入 docker 目录
cd docker

# 运行主程序
echo "🚀 启动网球分析..."
docker-compose run --rm tennis-analysis python main.py

echo "✅ 分析完成！结果已保存到 output_videos/ 目录"
