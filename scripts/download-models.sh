#!/bin/bash

# 模型下载脚本
# 作者: GitHub Copilot

set -e

echo "📥 下载网球分析所需的模型文件..."

# 创建模型目录
mkdir -p models

# 下载预训练的YOLOv8模型（用于人员检测）
echo "📥 下载 YOLOv8 人员检测模型..."
if [[ ! -f "models/yolov8x.pt" ]]; then
    wget -O models/yolov8x.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt
    echo "✅ YOLOv8 模型下载完成"
else
    echo "✅ YOLOv8 模型已存在"
fi

# 提示用户关于其他模型
echo ""
echo "⚠️  注意：以下模型需要手动获取："
echo ""
echo "1. 网球检测模型 (models/yolo5_last.pt):"
echo "   - 可以使用 training/tennis_ball_detector_training.ipynb 训练"
echo "   - 或从项目提供的链接下载"
echo ""
echo "2. 球场关键点检测模型 (models/keypoints_model.pth):"
echo "   - 可以使用 training/tennis_court_keypoints_training.ipynb 训练"
echo "   - 或从项目提供的链接下载"
echo ""
echo "📚 请查看项目 README.md 获取更多信息"
