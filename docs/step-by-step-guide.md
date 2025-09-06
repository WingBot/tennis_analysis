# 网球分析系统 - 逐步运行指南

## 📋 目录
1. [环境准备](#环境准备)
2. [快速开始](#快速开始)
3. [详细步骤](#详细步骤)
4. [测试验证](#测试验证)
5. [故障排除](#故障排除)
6. [进阶使用](#进阶使用)

## 🚀 环境准备

### 系统要求
- Linux/MacOS/Windows (推荐 Linux)
- Docker Engine 20.10+
- 至少 8GB RAM
- 至少 10GB 可用磁盘空间

### 验证环境
```bash
# 检查Docker是否安装
docker --version

# 检查可用空间
df -h

# 检查内存
free -h
```

## ⚡ 快速开始

### 一键运行测试
```bash
# 1. 进入项目目录
cd /home/czzr/Project/tennis_sys/tennis_analysis

# 2. 使用一键脚本
./start.sh

# 选择选项：
# 7) 下载模型文件 (首次运行必须)
# 5) 运行网球分析
```

### 快速测试命令
```bash
# 运行简化测试版本（推荐首次使用）
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py
```

## 📝 详细步骤

### 步骤1: 检查项目结构
```bash
cd /home/czzr/Project/tennis_sys/tennis_analysis
ls -la

# 应该看到以下重要目录：
# ├── input_videos/     # 输入视频
# ├── output_videos/    # 输出结果
# ├── models/          # 模型文件
# ├── tracker_stubs/   # 预处理数据
# ├── main.py          # 主程序
# ├── main_test.py     # 测试版本
# └── start.sh         # 一键脚本
```

### 步骤2: 检查Docker镜像
```bash
# 查看可用镜像
docker images | grep tennis

# 应该看到：
# tennis-analysis          latest    xxx    3.56GB
# docker_tennis-analysis   latest    xxx    6.67GB
```

### 步骤3: 验证依赖环境
```bash
# 测试容器环境
docker run --rm tennis-analysis:latest python -c "
import cv2
import torch
import ultralytics
print('✅ OpenCV版本:', cv2.__version__)
print('✅ PyTorch版本:', torch.__version__)
print('✅ Ultralytics版本:', ultralytics.__version__)
"
```

### 步骤4: 检查输入文件
```bash
# 查看输入视频
ls -la input_videos/

# 应该看到：
# input_video.mp4  (约13MB)
# image.png        (约3MB)
```

### 步骤5: 下载模型文件
```bash
# 方法1: 使用一键脚本
./start.sh
# 选择: 7) 下载模型文件

# 方法2: 手动下载
wget -O models/yolov8x.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt

# 验证模型文件
ls -la models/
# 应该看到: yolov8x.pt (约131MB)
```

### 步骤6: 运行测试版本
```bash
# 运行简化测试（推荐）
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py

# 成功标志：
# 🎾 启动网球分析程序...
# ✅ 视频读取完成，共 214 帧
# ✅ 球员检测数据加载完成
# ✅ 球检测数据加载完成
# ✅ 测试视频保存完成: output_videos/output_video_test.avi
```

### 步骤7: 检查输出结果
```bash
# 查看输出文件
ls -la output_videos/

# 应该看到新生成的文件：
# output_video_test.avi  (约9MB)
```

## ✅ 测试验证

### 基础验证清单
- [ ] Docker环境正常
- [ ] 项目文件完整
- [ ] 输入视频存在
- [ ] 模型文件下载
- [ ] 测试程序成功运行
- [ ] 输出视频生成

### 功能验证
```bash
# 1. 验证视频信息
ffprobe -v quiet -print_format json -show_format output_videos/output_video_test.avi

# 2. 验证视频可播放
ffplay output_videos/output_video_test.avi  # Linux
# 或在文件管理器中打开

# 3. 检查视频内容
# 应该看到：
# - 绿色矩形框标记球员
# - 黄色圆点标记网球
# - 左上角显示帧数
```

### 性能验证
```bash
# 检查处理时间
time docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py

# 正常情况下应该在1-5分钟内完成
```

## 🔧 故障排除

### 常见问题

#### 1. Docker镜像不存在
```bash
# 错误: Unable to find image 'tennis-analysis:latest'
# 解决: 构建镜像
./start.sh
# 选择: 1) 构建基础镜像
# 然后: 4) 生成最终生产镜像
```

#### 2. 模型文件缺失
```bash
# 错误: NotImplementedError: '' model loading not implemented
# 解决: 下载模型
./start.sh
# 选择: 7) 下载模型文件
```

#### 3. 内存不足
```bash
# 错误: Killed (OOM)
# 解决: 限制处理帧数
# 编辑 main_test.py，修改：
# for frame_num, frame in enumerate(video_frames[:10]):  # 只处理10帧
```

#### 4. 磁盘空间不足
```bash
# 检查空间
df -h

# 清理Docker
docker system prune -f

# 删除旧的输出文件
rm output_videos/output_video_test.avi
```

#### 5. 权限问题
```bash
# 错误: Permission denied
# 解决: 检查文件权限
sudo chown -R $USER:$USER /home/czzr/Project/tennis_sys/
chmod +x start.sh
```

### 日志调试
```bash
# 查看详细日志
docker run -it --rm \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py 2>&1 | tee debug.log

# 检查特定错误
grep -i error debug.log
grep -i traceback debug.log
```

## 🎯 进阶使用

### 运行完整版本
```bash
# 需要先训练/下载所有模型
# models/yolo5_last.pt
# models/keypoints_model.pth

# 然后运行完整程序
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/models:/app/models \
  tennis-analysis:latest python main.py
```

### 自定义输入视频
```bash
# 1. 将视频文件放入 input_videos/
cp /path/to/your/video.mp4 input_videos/my_video.mp4

# 2. 修改程序中的视频路径
# 编辑 main_test.py 第18行：
# input_video_path = "input_videos/my_video.mp4"

# 3. 运行分析
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py
```

### 开发模式
```bash
# 启动Jupyter Lab进行开发
docker run -it --rm -p 8888:8888 \
  -v $(pwd):/app \
  tennis-analysis:latest \
  jupyter lab --ip=0.0.0.0 --allow-root --no-browser

# 浏览器访问: http://localhost:8888
```

### 批量处理
```bash
# 处理多个视频
for video in input_videos/*.mp4; do
  echo "处理: $video"
  # 修改程序配置并运行
  docker run -it --rm \
    -v $(pwd):/app \
    tennis-analysis:latest python main_test.py
done
```

## 📊 输出说明

### 输出文件类型
- `output_video_test.avi` - 带检测标记的视频
- `debug.log` - 运行日志（如果生成）
- `screenshot.jpeg` - 截图（可能存在）

### 视频内容说明
- **绿色矩形框**: 检测到的球员
- **黄色圆点**: 检测到的网球位置
- **帧数显示**: 左上角的当前帧编号
- **Player ID**: 球员标识编号

### 性能指标
- 处理速度: 约10-20 FPS
- 内存使用: 2-4GB
- 输出大小: 约为输入的70%

## 🔗 相关链接
- [项目主页](../README.md)
- [训练指南](training-guide.md) 
- [API文档](api-reference.md)
- [常见问题](faq.md)

---

**创建日期**: 2025年9月7日  
**版本**: 1.0  
**维护者**: Tennis Analysis Team
