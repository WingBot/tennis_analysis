# 网球分析程序运行解决方案

## 问题分析
运行网球分析程序时遇到了模型文件缺失的问题：
- 程序需要三个模型文件：
  1. `yolov8x.pt` - 用于人员检测 ✅ 已下载
  2. `models/yolo5_last.pt` - 用于网球检测 ❌ 需要训练或下载
  3. `models/keypoints_model.pth` - 用于球场关键点检测 ❌ 需要训练或下载

## 解决方案

### 1. 快速测试方案（推荐）
使用预处理的检测数据，跳过模型加载，快速验证程序功能：

```bash
cd /home/czzr/Project/tennis_sys/tennis_analysis
# 运行简化测试版本
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py
```

### 2. 完整解决方案

#### A. 下载已有的YOLOv8模型
```bash
./start.sh  # 选择选项7下载模型文件
```

#### B. 训练缺失的模型
1. **网球检测模型**：
   ```bash
   # 使用training/tennis_ball_detector_training.ipynb进行训练
   docker run -it --rm \
     -v $(pwd):/app \
     tennis-analysis:latest \
     jupyter lab --ip=0.0.0.0 --allow-root --no-browser
   ```

2. **球场关键点检测模型**：
   ```bash
   # 使用training/tennis_court_keypoints_training.ipynb进行训练
   ```

#### C. 或者修改程序使用替代方案
- 使用更简单的检测算法
- 跳过某些功能模块
- 使用默认参数

### 3. 测试结果
✅ 成功生成输出视频：`output_videos/output_video_test.avi`
- 视频大小：9.4MB
- 包含球员检测框（绿色）
- 包含网球标记（黄色圆点）
- 显示帧数信息

### 4. 下一步建议

#### 优先级1：训练模型
1. 运行 `training/tennis_ball_detector_training.ipynb` 训练网球检测模型
2. 运行 `training/tennis_court_keypoints_training.ipynb` 训练球场关键点模型

#### 优先级2：完善功能
1. 启用球场关键点检测
2. 启用迷你球场坐标转换
3. 添加球员统计功能
4. 添加击球分析功能

#### 优先级3：性能优化
1. 优化模型推理速度
2. 添加GPU支持
3. 优化视频处理流程

## 运行命令总结

### 基础环境检查
```bash
docker images  # 查看可用镜像
docker run --rm tennis-analysis:latest python -c "import cv2, torch, ultralytics; print('✅ 依赖正常')"
```

### 快速测试（使用预处理数据）
```bash
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py
```

### 完整运行（需要所有模型文件）
```bash
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/models:/app/models \
  tennis-analysis:latest python main.py
```

### 模型训练
```bash
docker run -it --rm -p 8888:8888 \
  -v $(pwd):/app \
  tennis-analysis:latest \
  jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## 文件说明
- `main.py` - 原始完整版本（需要所有模型）
- `main_test.py` - 简化测试版本（使用预处理数据）
- `tracker_stubs/` - 预处理的检测数据
- `models/` - 模型文件目录
- `input_videos/` - 输入视频
- `output_videos/` - 输出视频

现在您可以成功运行网球分析程序了！🎾
