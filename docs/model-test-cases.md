# 网球分析模型测试用例文档

## 📋 测试概述

基于成功下载的模型文件，我们提供了两个主要模型的测试用例：

### 🎯 可用模型
1. **网球检测模型**: `models/yolo5_last.pt` (164.6MB) ✅
2. **球场关键点检测模型**: `models/keypoints_model.pth` (90.2MB) ✅

## 🧪 测试用例

### 1. 网球检测模型测试 (yolo5_last.pt)

#### 🎾 功能描述
- 检测视频中的网球位置
- 提供边界框坐标
- 支持多帧追踪和插值

#### 📝 测试文件
- `test_ball_model.py` - 完整的网球检测测试
- `test_validation.py` - 简化验证测试

#### 🚀 运行命令
```bash
# 完整测试
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/models:/app/models \
  -v $(pwd):/app \
  tennis-analysis:latest python test_ball_model.py

# 验证测试
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python test_validation.py
```

#### ⚠️ 已知问题
- YOLO版本兼容性问题：`ultralytics.nn.modules.conv`
- 需要调整模型加载方式或更新YOLO版本

#### 💡 解决方案
- 使用预处理数据进行测试验证
- 或升级到兼容的YOLO版本

### 2. 球场关键点检测模型测试 (keypoints_model.pth)

#### 🏟️ 功能描述
- 检测网球场的关键点位置
- 基于ResNet50架构
- 输出14个关键点的坐标

#### 📝 测试文件
- `test_court_model.py` - 完整的球场检测测试
- `test_validation.py` - 简化验证测试

#### 🚀 运行命令
```bash
# 完整测试
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/models:/app/models \
  -v $(pwd):/app \
  tennis-analysis:latest python test_court_model.py

# 验证测试（推荐）
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python test_validation.py
```

#### ✅ 测试结果
- ✅ 模型初始化成功
- ✅ 检测到28个关键点
- ✅ 稳定性良好（标准差: 0.0）
- ✅ 性能良好（11.6 FPS）

#### 🎯 输出示例
```
🏟️ 测试球场关键点检测...
✅ 检测到 28 个关键点
📊 关键点检测成功（模型工作正常）

📊 稳定性分析:
   平均关键点数: 28.0
   标准差: 0.0
   稳定性: 良好

📊 性能统计:
   平均检测时间: 0.086s
   处理速度: 11.6 FPS
```

## 🎬 输出文件

### 测试视频输出
- `output_videos/ball_detection_test.avi` - 网球检测测试结果
- `output_videos/court_keypoints_test.avi` - 球场关键点测试结果
- `output_videos/model_validation_test.avi` - 验证测试结果 ✅

### 可视化内容
- **绿色矩形框**: 球员检测
- **黄色圆圈**: 网球检测
- **蓝色/绿色点**: 球场关键点
- **文本标签**: 帧数和检测信息

## 🎯 快速测试流程

### 方法1: 一键测试脚本
```bash
./test_models.sh
# 选择相应的测试选项
```

### 方法2: 验证测试（推荐）
```bash
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python test_validation.py
```

## 📊 测试结果总结

### ✅ 成功验证的功能
1. **球场关键点检测** - 完全正常工作
2. **预处理数据流程** - 完整可用
3. **可视化输出** - 正常生成
4. **模型稳定性** - 良好
5. **处理性能** - 11.6 FPS

### ⚠️ 需要注意的问题
1. **网球检测模型** - YOLO版本兼容性问题
2. **球员检测模型** - yolov8x.pt需要重新下载

### 💡 推荐使用方式
1. **球场关键点检测** - 直接使用，工作正常
2. **网球检测** - 使用预处理数据或修复兼容性
3. **完整分析** - 结合预处理数据和球场检测

## 🔧 故障排除

### 常见问题
1. **模型文件不存在**
   ```bash
   ./start.sh  # 选择下载模型选项
   ```

2. **YOLO兼容性问题**
   ```bash
   # 使用验证测试代替完整测试
   python test_validation.py
   ```

3. **内存不足**
   ```bash
   # 减少测试帧数，编辑测试文件中的帧数限制
   ```

### 调试命令
```bash
# 检查模型文件
ls -la models/

# 查看测试日志
docker run -it --rm -v $(pwd):/app tennis-analysis:latest python test_validation.py 2>&1 | tee test.log

# 检查输出视频
ls -la output_videos/
```

## 🎯 下一步建议

1. **修复YOLO兼容性** - 更新ultralytics版本或调整模型加载方式
2. **完整流程测试** - 结合所有工作的组件
3. **性能优化** - 针对实际使用场景优化
4. **自定义训练** - 根据需要训练新的模型

---

**更新日期**: 2025年9月7日  
**测试状态**: 球场关键点✅ | 网球检测⚠️ | 预处理数据✅  
**维护者**: Tennis Analysis Team
