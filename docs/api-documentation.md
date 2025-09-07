# 📚 API文档

## 概述

本文档描述了网球分析系统的主要API接口和使用方法。

## 主要程序

### main_working.py

完整的网球分析程序，集成了所有功能模块。

```python
def main():
    """
    主分析函数
    功能:
    - 视频读取和处理
    - 球员和球的检测
    - 球场关键点检测
    - 统计数据计算
    - 输出视频生成
    
    输入: input_videos/input_video.mp4
    输出: output_videos/output_video_complete.avi
    """
```

**使用方法:**
```bash
python main_working.py
```

### test_validation.py

简化验证程序，用于测试基础功能。

```python
def validation_test():
    """
    验证测试函数
    功能:
    - 基础组件测试
    - 预处理数据验证
    - 快速功能验证
    
    输出: output_videos/model_validation_test.avi
    """
```

## 核心模块

### court_line_detector.py

球场线检测模块

```python
class CourtLineDetector:
    def __init__(self, model_path):
        """
        初始化球场检测器
        参数:
            model_path (str): 模型文件路径
        """
    
    def predict(self, frame):
        """
        检测球场关键点
        参数:
            frame (np.ndarray): 输入视频帧
        返回:
            np.ndarray: 球场关键点坐标 (N, 2)
        """
```

### ball_tracker.py

球追踪模块

```python
class BallTracker:
    def detect_frames(self, frames):
        """
        检测视频帧中的球
        参数:
            frames (list): 视频帧列表
        返回:
            list: 检测结果列表
        """
```

### player_tracker.py

球员追踪模块

```python
class PlayerTracker:
    def detect_frames(self, frames):
        """
        检测视频帧中的球员
        参数:
            frames (list): 视频帧列表
        返回:
            list: 检测结果列表
        """
```

### mini_court.py

迷你球场可视化模块

```python
class MiniCourt:
    def __init__(self, frame):
        """
        初始化迷你球场
        参数:
            frame (np.ndarray): 参考视频帧
        """
    
    def draw_mini_court(self, frame):
        """
        绘制迷你球场
        参数:
            frame (np.ndarray): 目标视频帧
        """
```

## 工具函数

### utils/video_utils.py

```python
def read_video(video_path):
    """
    读取视频文件
    参数:
        video_path (str): 视频文件路径
    返回:
        list: 视频帧列表
    """

def save_video(output_video_frames, output_video_path):
    """
    保存视频文件
    参数:
        output_video_frames (list): 输出帧列表
        output_video_path (str): 输出路径
    """
```

### utils/bbox_utils.py

```python
def get_center_of_bbox(bbox):
    """
    获取边界框中心点
    参数:
        bbox (list): [x1, y1, x2, y2]
    返回:
        tuple: (center_x, center_y)
    """

def measure_distance(p1, p2):
    """
    计算两点间距离
    参数:
        p1, p2 (tuple): 坐标点
    返回:
        float: 距离值
    """
```

### utils/conversions.py

```python
def convert_pixel_distance_to_meters(pixel_distance, reference_height_in_pixels, reference_height_in_meters):
    """
    像素距离转换为实际距离
    参数:
        pixel_distance (float): 像素距离
        reference_height_in_pixels (float): 参考高度(像素)
        reference_height_in_meters (float): 参考高度(米)
    返回:
        float: 实际距离(米)
    """
```

## 数据格式

### 检测结果格式

```python
# 球员检测结果
player_detections = [
    {
        1: [x1, y1, x2, y2],  # 球员1边界框
        2: [x1, y1, x2, y2],  # 球员2边界框
    },
    # ... 每帧的检测结果
]

# 球检测结果  
ball_detections = [
    {
        1: [x1, y1, x2, y2]  # 球的边界框
    },
    # ... 每帧的检测结果
]

# 球场关键点
court_keypoints = [
    [x1, y1],  # 关键点1
    [x2, y2],  # 关键点2
    # ... 共14个关键点
]
```

### 统计数据格式

```python
player_stats = {
    'frame_num': int,
    'player_1_number_of_shots': int,
    'player_1_total_shot_speed': float,
    'player_1_last_shot_speed': float,
    'player_1_total_player_speed': float,
    'player_1_last_player_speed': float,
    'player_2_number_of_shots': int,
    'player_2_total_shot_speed': float,
    'player_2_last_shot_speed': float,
    'player_2_total_player_speed': float,
    'player_2_last_player_speed': float,
}
```

## 配置参数

### constants.py

```python
# 球场尺寸相关
DOUBLE_LINE_WIDTH = 10.97  # 双打线宽度(米)
SINGLE_LINE_WIDTH = 8.23   # 单打线宽度(米)

# 视频处理参数
VIDEO_FPS = 24            # 视频帧率
BATCH_SIZE = 50          # 批处理大小

# 模型路径
YOLO_MODEL_PATH = "models/yolov8x.pt"
BALL_MODEL_PATH = "models/yolo5_last.pt"
COURT_MODEL_PATH = "models/keypoints_model.pth"
```

## 性能指标

| 指标 | 值 |
|------|-----|
| 处理速度 | 11.6 FPS |
| 球场关键点检测精度 | 28个特征点 |
| 支持视频格式 | MP4, AVI |
| 输出格式 | AVI (H.264) |
| 内存需求 | 4-8GB |
| 处理时间 | ~2-3分钟 (214帧) |

## 错误代码

| 代码 | 含义 | 解决方案 |
|------|------|----------|
| E001 | 模型文件未找到 | 检查models/目录 |
| E002 | 视频文件读取失败 | 检查视频格式 |
| E003 | CUDA内存不足 | 使用CPU模式 |
| E004 | 依赖包缺失 | 重新安装依赖 |

## 示例代码

### 基础使用

```python
from utils import read_video, save_video
from court_line_detector import CourtLineDetector

# 读取视频
frames = read_video("input_videos/input_video.mp4")

# 检测球场
detector = CourtLineDetector("models/keypoints_model.pth")
keypoints = detector.predict(frames[0])

# 保存结果
save_video(frames, "output_videos/result.avi")
```

### 自定义配置

```python
import os

# 设置环境变量
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # 使用GPU 0
os.environ['OMP_NUM_THREADS'] = '4'       # 4线程CPU

# 运行分析
exec(open('main_working.py').read())
```

## 扩展开发

### 添加新的检测器

```python
class CustomDetector:
    def __init__(self, model_path):
        self.model = load_model(model_path)
    
    def detect(self, frame):
        # 实现检测逻辑
        return results
```

### 自定义统计指标

```python
def calculate_custom_stats(detections):
    """
    计算自定义统计指标
    """
    # 实现统计逻辑
    return stats
```

---

**版本:** v2.0  
**更新日期:** 2024年9月8日
