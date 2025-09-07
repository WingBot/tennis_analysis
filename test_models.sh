#!/bin/bash
# 网球分析模型测试脚本

echo "🎾 网球分析模型测试套件"
echo "=========================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# 检查模型文件
echo ""
echo "📁 检查模型文件..."
if [ -f "models/yolo5_last.pt" ]; then
    success "网球检测模型存在: models/yolo5_last.pt"
else
    error "网球检测模型缺失: models/yolo5_last.pt"
    exit 1
fi

if [ -f "models/keypoints_model.pth" ]; then
    success "球场关键点模型存在: models/keypoints_model.pth"
else
    error "球场关键点模型缺失: models/keypoints_model.pth"
    exit 1
fi

if [ -f "models/yolov8x.pt" ]; then
    success "球员检测模型存在: models/yolov8x.pt"
else
    warning "球员检测模型缺失，将使用预训练模型"
fi

echo ""
echo "🎯 可用的测试选项:"
echo "1) 测试网球检测模型 (yolo5_last.pt)"
echo "2) 测试球场关键点模型 (keypoints_model.pth)" 
echo "3) 完整模型集成测试"
echo "4) 运行所有测试"
echo "5) 退出"

read -p "请选择测试选项 (1-5): " choice

case $choice in
    1)
        echo ""
        info "开始网球检测模型测试..."
        docker run -it --rm \
            -v $(pwd)/input_videos:/app/input_videos \
            -v $(pwd)/output_videos:/app/output_videos \
            -v $(pwd)/models:/app/models \
            -v $(pwd):/app \
            tennis-analysis:latest python test_ball_model.py
        ;;
    2)
        echo ""
        info "开始球场关键点模型测试..."
        docker run -it --rm \
            -v $(pwd)/input_videos:/app/input_videos \
            -v $(pwd)/output_videos:/app/output_videos \
            -v $(pwd)/models:/app/models \
            -v $(pwd):/app \
            tennis-analysis:latest python test_court_model.py
        ;;
    3)
        echo ""
        info "开始完整模型集成测试..."
        docker run -it --rm \
            -v $(pwd)/input_videos:/app/input_videos \
            -v $(pwd)/output_videos:/app/output_videos \
            -v $(pwd)/models:/app/models \
            -v $(pwd):/app \
            tennis-analysis:latest python test_complete_models.py
        ;;
    4)
        echo ""
        info "运行所有测试..."
        
        echo ""
        echo "🎾 测试1: 网球检测模型"
        echo "----------------------"
        docker run -it --rm \
            -v $(pwd)/input_videos:/app/input_videos \
            -v $(pwd)/output_videos:/app/output_videos \
            -v $(pwd)/models:/app/models \
            -v $(pwd):/app \
            tennis-analysis:latest python test_ball_model.py
        
        echo ""
        echo "🏟️ 测试2: 球场关键点模型"
        echo "------------------------"
        docker run -it --rm \
            -v $(pwd)/input_videos:/app/input_videos \
            -v $(pwd)/output_videos:/app/output_videos \
            -v $(pwd)/models:/app/models \
            -v $(pwd):/app \
            tennis-analysis:latest python test_court_model.py
        
        echo ""
        echo "🎯 测试3: 完整集成测试"
        echo "---------------------"
        docker run -it --rm \
            -v $(pwd)/input_videos:/app/input_videos \
            -v $(pwd)/output_videos:/app/output_videos \
            -v $(pwd)/models:/app/models \
            -v $(pwd):/app \
            tennis-analysis:latest python test_complete_models.py
        
        echo ""
        success "所有测试完成！"
        ;;
    5)
        echo "退出测试"
        exit 0
        ;;
    *)
        error "无效选择"
        exit 1
        ;;
esac

echo ""
echo "📺 测试完成！请查看输出视频:"
echo "   - output_videos/ball_detection_test.avi (网球检测)"
echo "   - output_videos/court_keypoints_test.avi (球场关键点)"
echo "   - output_videos/complete_model_test.avi (完整集成)"

echo ""
echo "💡 测试结果说明:"
echo "   - 绿色框: 球员检测"
echo "   - 黄色圆圈: 网球检测"
echo "   - 蓝色/绿色点: 球场关键点"
echo "   - 红色'SHOT!': 击球时刻"

echo ""
success "模型测试全部完成！"
