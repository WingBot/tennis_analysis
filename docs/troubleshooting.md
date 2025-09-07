# 🔧 故障排除详细指南

## 📋 目录
- [环境相关问题](#环境相关问题)
- [模型相关问题](#模型相关问题)
- [运行时错误](#运行时错误)
- [性能问题](#性能问题)
- [输出问题](#输出问题)
- [调试技巧](#调试技巧)

## 🐳 环境相关问题

### 问题1: Docker未安装或未启动
**症状:**
```bash
docker: command not found
# 或
Cannot connect to the Docker daemon
```

**解决方案:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# 添加用户到docker组
sudo usermod -aG docker $USER
newgrp docker
```

### 问题2: Docker镜像缺失
**症状:**
```bash
Unable to find image 'tennis-analysis:latest' locally
```

**解决方案:**
```bash
# 方案1: 构建本地镜像
cd /home/czzr/Project/tennis_sys/tennis_analysis
docker build -t tennis-analysis:latest .

# 方案2: 使用替代镜像
docker pull python:3.8
docker run --rm -v "$PWD":/workspace -w /workspace python:3.8 bash -c "pip install opencv-python torch torchvision pandas numpy && python main_working.py"
```

### 问题3: 权限问题
**症状:**
```bash
Permission denied while trying to connect to the Docker daemon socket
```

**解决方案:**
```bash
# 临时解决
sudo docker run ...

# 永久解决
sudo usermod -aG docker $USER
logout
# 重新登录
```

## 🤖 模型相关问题

### 问题1: 模型文件下载失败
**症状:**
```bash
wget: unable to resolve host address
# 或
FileNotFoundError: [Errno 2] No such file or directory: 'models/yolov8x.pt'
```

**解决方案:**
```bash
# 检查网络连接
ping github.com

# 手动下载模型文件
cd models/

# YOLOv8模型
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt

# 如果github访问困难，使用镜像源
wget https://ghproxy.com/https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt

# 验证文件完整性
ls -lh models/
md5sum models/*.pt
```

### 问题2: 模型加载失败
**症状:**
```bash
ModuleNotFoundError: No module named 'ultralytics.nn.modules.conv'
# 或
RuntimeError: Error(s) in loading state_dict
```

**解决方案:**
```bash
# 使用兼容版本
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python main_working.py

# 如果还是失败，使用纯预处理数据版本
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python test_validation.py
```

### 问题3: CUDA版本不匹配
**症状:**
```bash
RuntimeError: CUDA error: no kernel image is available for execution on the device
```

**解决方案:**
```bash
# 强制使用CPU
export CUDA_VISIBLE_DEVICES=""
docker run --rm -e CUDA_VISIBLE_DEVICES="" -v "$PWD":/workspace -w /workspace tennis-analysis:latest python main_working.py

# 或修改代码强制CPU模式
sed -i 's/device="cuda"/device="cpu"/g' *.py
```

## ⚡ 运行时错误

### 问题1: 内存不足
**症状:**
```bash
CUDA out of memory
# 或
MemoryError: Unable to allocate array
```

**解决方案:**
```bash
# 增加Docker内存限制
docker run --rm --memory=8g -v "$PWD":/workspace -w /workspace tennis-analysis:latest python main_working.py

# 减少批处理大小
# 编辑代码，减少一次处理的帧数
```

### 问题2: 视频文件格式问题
**症状:**
```bash
OpenCV Error: Unable to open video file
# 或
IndexError: list index out of range
```

**解决方案:**
```bash
# 检查视频文件
ls -la input_videos/
file input_videos/input_video.mp4

# 转换视频格式
ffmpeg -i input_videos/original.mp4 -c:v libx264 -c:a aac input_videos/input_video.mp4

# 验证视频可读性
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python -c "
import cv2
cap = cv2.VideoCapture('input_videos/input_video.mp4')
print('Video readable:', cap.isOpened())
print('Frame count:', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
cap.release()
"
```

### 问题3: 依赖包冲突
**症状:**
```bash
ImportError: cannot import name 'xxx' from 'yyy'
# 或
AttributeError: module 'cv2' has no attribute 'xxx'
```

**解决方案:**
```bash
# 检查包版本
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest pip list

# 重新安装包
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest pip install --upgrade opencv-python

# 使用固定版本
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest pip install opencv-python==4.8.0.74
```

## 🚀 性能问题

### 问题1: 处理速度太慢
**当前状态:** 11.6 FPS处理速度

**优化方案:**
```bash
# 1. 使用GPU加速
docker run --gpus all --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python main_working.py

# 2. 减少视频分辨率
ffmpeg -i input_videos/input_video.mp4 -vf scale=640:480 input_videos/input_video_small.mp4

# 3. 跳帧处理
ffmpeg -i input_videos/input_video.mp4 -vf "select=not(mod(n\,2))" -vsync vfr input_videos/input_video_half.mp4

# 4. 使用多线程
export OMP_NUM_THREADS=4
```

### 问题2: 内存使用过高
**解决方案:**
```bash
# 监控内存使用
docker stats

# 分批处理视频
python -c "
import cv2
cap = cv2.VideoCapture('input_videos/input_video.mp4')
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
batch_size = 50
for i in range(0, total_frames, batch_size):
    print(f'Processing batch {i}-{i+batch_size}')
"
```

## 📁 输出问题

### 问题1: 视频编码失败
**症状:**
```bash
OpenCV: FFMPEG: tag 0x5634504d/'MP4V' is not supported with codec id 12 and format 'mp4'
```

**解决方案:**
```bash
# 安装额外编解码器
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest apt-get update && apt-get install -y ffmpeg

# 修改编码格式
# 在代码中将 fourcc = cv2.VideoWriter_fourcc(*'MP4V') 
# 改为 fourcc = cv2.VideoWriter_fourcc(*'XVID')
```

### 问题2: 输出文件损坏
**症状:**
```bash
# 文件大小为0或无法播放
ls -la output_videos/
```

**解决方案:**
```bash
# 检查磁盘空间
df -h

# 验证文件完整性
file output_videos/output_video_complete.avi

# 使用不同的编码器
ffmpeg -i output_videos/output_video_complete.avi -c:v libx264 output_videos/output_video_fixed.mp4
```

## 🔍 调试技巧

### 1. 详细日志输出
```python
# 在Python代码中添加调试信息
import logging
logging.basicConfig(level=logging.DEBUG)

# 打印变量状态
print(f"Video frames: {len(video_frames)}")
print(f"Player detections: {len(player_detections)}")
print(f"Ball detections: {len(ball_detections)}")
```

### 2. 逐步执行
```bash
# 创建调试版本
cp main_working.py main_debug.py

# 添加断点和输出
# 注释掉某些步骤，逐步验证
```

### 3. 单元测试
```bash
# 测试各个组件
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python test_court_model.py
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python test_ball_model.py

# 验证输入数据
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python -c "
import pickle
with open('tracker_stubs/player_detections.pkl', 'rb') as f:
    data = pickle.load(f)
print('Player detections loaded:', len(data))
"
```

### 4. 性能分析
```python
# 添加计时代码
import time
start_time = time.time()
# ... 执行代码 ...
print(f"Execution time: {time.time() - start_time:.2f} seconds")
```

## 📊 验证清单

运行前检查：
- [ ] Docker正常运行
- [ ] 所有模型文件存在且大小正确
- [ ] 输入视频文件可访问
- [ ] 有足够的磁盘空间 (>2GB)
- [ ] 预处理数据文件存在

运行时监控：
- [ ] 无错误日志输出
- [ ] 内存使用率 <80%
- [ ] 处理进度正常显示
- [ ] 临时文件正常创建

运行后验证：
- [ ] 输出视频文件生成
- [ ] 文件大小合理 (>10MB)
- [ ] 视频可正常播放
- [ ] 分析统计数据合理

## 🆘 紧急恢复

如果所有方法都失败：

```bash
# 1. 重置环境
docker system prune -a
cd /home/czzr/Project/tennis_sys/tennis_analysis

# 2. 使用最简单的验证版本
docker run --rm -v "$PWD":/workspace -w /workspace python:3.8 bash -c "
pip install opencv-python numpy pandas
python test_validation.py
"

# 3. 检查基础功能
docker run --rm -v "$PWD":/workspace -w /workspace python:3.8 bash -c "
pip install opencv-python
python -c 'import cv2; print(cv2.__version__)'
"
```

---

**紧急联系:** 如果问题依然存在，请提供完整的错误日志和系统信息进行进一步诊断。
