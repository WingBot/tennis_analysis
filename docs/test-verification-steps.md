# 网球分析系统测试验证步骤

## 快速验证流程

### 1. 环境检查
```bash
cd /home/czzr/Project/tennis_sys/tennis_analysis
docker --version
ls -la
```

### 2. 验证依赖
```bash
docker run --rm tennis-analysis:latest python -c "
import cv2, torch, ultralytics
print('✅ 所有依赖正常')
print('OpenCV:', cv2.__version__)
print('PyTorch:', torch.__version__)
"
```

### 3. 检查输入文件
```bash
ls -la input_videos/
# 确保看到: input_video.mp4 (约13MB)
```

### 4. 下载模型（首次运行）
```bash
./start.sh
# 选择: 7) 下载模型文件
# 等待下载完成: yolov8x.pt (131MB)
```

### 5. 运行测试程序
```bash
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py
```

### 6. 验证输出
```bash
ls -la output_videos/
# 确保看到: output_video_test.avi (约9MB)
```

## 成功标志

运行时应该看到以下输出：
```
🎾 启动网球分析程序...
📹 读取视频: input_videos/input_video.mp4
✅ 视频读取完成，共 214 帧
📦 加载预处理的检测数据...
✅ 球员检测数据加载完成
✅ 球检测数据加载完成
🔄 手动进行球位置插值...
✅ 球位置插值完成
⚠️ 跳过球场关键点检测（需要模型文件）
🏃 处理球员选择...
🏟️ 创建迷你球场...
🎾 简化击球检测...
✅ 模拟发现 22 个击球时刻
📍 跳过坐标转换到迷你球场...
📊 处理统计数据...
🎬 处理视频帧...
💾 保存输出视频...
✅ 测试视频保存完成: output_videos/output_video_test.avi
```

## 常见问题解决

### Docker镜像不存在
```bash
# 构建镜像
./start.sh
# 选择: 1) 构建基础镜像
# 然后: 4) 生成最终生产镜像
```

### 模型文件缺失
```bash
# 下载模型
./start.sh
# 选择: 7) 下载模型文件
```

### 权限问题
```bash
sudo chown -R $USER:$USER .
chmod +x start.sh
```

### 内存不足
```bash
# 编辑 main_test.py，减少处理帧数
# 第125行改为: for frame_num, frame in enumerate(video_frames[:10]):
```

## 输出视频内容

生成的视频应包含：
- 绿色矩形框：标记检测到的球员
- 黄色圆点：标记网球位置  
- 帧数显示：左上角显示当前帧数
- Player ID：球员标识号

## 下一步

测试成功后，可以：
1. 尝试使用自己的视频文件
2. 训练完整的模型
3. 运行完整版本的分析程序
4. 开发自定义功能

---
**测试完成时间**: $(date)
**测试状态**: ✅ 通过 / ❌ 失败
**备注**: 记录任何问题或改进建议
