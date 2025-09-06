#!/bin/bash
# 网球分析系统 - 快速测试脚本
# 使用方法: bash docs/quick-test.sh

echo "🎾 网球分析系统 - 快速测试"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试步骤计数
STEP=1

# 测试函数
test_step() {
    echo -e "\n${YELLOW}步骤 $STEP: $1${NC}"
    STEP=$((STEP + 1))
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# 开始测试
cd "$(dirname "$0")/.." || error "无法进入项目目录"

test_step "检查项目目录"
if [ -f "main.py" ] && [ -f "main_test.py" ]; then
    success "项目文件存在"
else
    error "项目文件缺失"
fi

test_step "检查Docker环境"
if command -v docker &> /dev/null; then
    success "Docker已安装: $(docker --version)"
else
    error "Docker未安装，请先安装Docker"
fi

test_step "检查Docker镜像"
if docker images | grep -q "tennis-analysis"; then
    success "Docker镜像存在"
else
    warning "Docker镜像不存在，尝试构建..."
    if [ -f "start.sh" ]; then
        chmod +x start.sh
        echo "请运行: ./start.sh 并选择构建镜像选项"
        exit 1
    else
        error "构建脚本不存在"
    fi
fi

test_step "检查输入文件"
if [ -f "input_videos/input_video.mp4" ]; then
    success "输入视频存在: $(ls -lh input_videos/input_video.mp4 | awk '{print $5}')"
else
    error "输入视频不存在"
fi

test_step "检查预处理数据"
if [ -f "tracker_stubs/player_detections.pkl" ] && [ -f "tracker_stubs/ball_detections.pkl" ]; then
    success "预处理数据存在"
else
    error "预处理数据缺失"
fi

test_step "验证Docker容器依赖"
echo "测试容器环境..."
if docker run --rm tennis-analysis:latest python -c "import cv2, torch, ultralytics; print('依赖检查通过')" 2>/dev/null; then
    success "容器依赖正常"
else
    error "容器依赖有问题"
fi

test_step "运行测试程序"
echo "开始运行网球分析测试..."
echo "这可能需要1-3分钟，请耐心等待..."

# 运行测试程序
if docker run -it --rm \
    -v "$(pwd)/input_videos:/app/input_videos" \
    -v "$(pwd)/output_videos:/app/output_videos" \
    -v "$(pwd)/tracker_stubs:/app/tracker_stubs" \
    -v "$(pwd):/app" \
    tennis-analysis:latest python main_test.py; then
    success "程序运行成功"
else
    error "程序运行失败"
fi

test_step "验证输出结果"
if [ -f "output_videos/output_video_test.avi" ]; then
    output_size=$(ls -lh output_videos/output_video_test.avi | awk '{print $5}')
    success "输出视频生成成功: $output_size"
    
    # 检查文件是否为空
    if [ -s "output_videos/output_video_test.avi" ]; then
        success "输出文件不为空"
    else
        error "输出文件为空"
    fi
else
    error "输出视频未生成"
fi

echo ""
echo "🎉 所有测试通过！"
echo "================================"
echo "✅ 测试结果:"
echo "   - 输入视频: input_videos/input_video.mp4"
echo "   - 输出视频: output_videos/output_video_test.avi"
echo ""
echo "📺 查看结果:"
echo "   可以使用视频播放器打开输出文件查看检测效果"
echo ""
echo "🚀 下一步:"
echo "   1. 查看输出视频验证检测效果"
echo "   2. 尝试使用自己的视频文件"
echo "   3. 训练完整模型获得更多功能"
echo ""
echo "📚 更多信息:"
echo "   - 详细指南: docs/step-by-step-guide.md"
echo "   - 验证步骤: docs/test-verification-steps.md"
echo "   - 项目说明: README.md"
