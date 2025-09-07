# 网球分析项目 Docker 开发环境

## 项目概述
这是一个基于深度学习的网球视频分析项目，可以检测球员、网球和球场线，并提供比赛统计分析。

## 🚀 快速开始

### 1. 构建 Docker 环境
```bash
./scripts/build.sh
```

### 2. 下载必要的模型
```bash
./scripts/download-models.sh
```

### 3. 准备输入视频
将您的网球视频文件放置在 `input_videos/` 目录下，并命名为 `input_video.mp4`

### 4. 运行分析
```bash
./scripts/run-main.sh
```

## 📋 可用脚本

| 脚本 | 功能 | 用法 |
|------|------|------|
| `scripts/build.sh` | 构建 Docker 镜像 | `./scripts/build.sh` |
| `scripts/run-dev.sh` | 启动开发环境 | `./scripts/run-dev.sh` |
| `scripts/run-main.sh` | 运行主程序 | `./scripts/run-main.sh` |
| `scripts/run-notebook.sh` | 启动 Jupyter | `./scripts/run-notebook.sh` |
| `scripts/download-models.sh` | 下载模型 | `./scripts/download-models.sh` |
| `scripts/cleanup.sh` | 清理环境 | `./scripts/cleanup.sh` |

## 🔧 开发模式

### 进入开发环境
```bash
./scripts/run-dev.sh
```

这将启动一个交互式的 Docker 容器，您可以在其中：
- 运行 Python 脚本
- 调试代码
- 安装额外的包
- 访问所有项目文件

### 启动 Jupyter Notebook
```bash
./scripts/run-notebook.sh
```

然后在浏览器中访问 `http://localhost:8888` 来使用 Jupyter Notebook。

## 📁 项目结构

```
tennis_analysis/
├── Dockerfile              # Docker 镜像定义
├── docker-compose.yml      # Docker Compose 配置
├── requirements.txt        # Python 依赖
├── main.py                 # 主程序
├── scripts/                # 构建和运行脚本
│   ├── build.sh           # 构建镜像
│   ├── run-dev.sh         # 开发环境
│   ├── run-main.sh        # 运行主程序
│   ├── run-notebook.sh    # Jupyter服务
│   ├── download-models.sh # 下载模型
│   └── cleanup.sh         # 清理环境
├── input_videos/          # 输入视频目录
├── output_videos/         # 输出视频目录
├── models/               # 模型文件目录
├── analysis/             # 分析 Notebook
├── training/             # 训练 Notebook
└── ...
```

## 🛠️ 所需模型

项目需要以下模型文件：

1. **YOLOv8 人员检测模型** (`models/yolov8x.pt`)
   - 自动下载：运行 `./scripts/download-models.sh`

2. **网球检测模型** (`models/yolo5_last.pt`)
   - 训练：使用 `training/tennis_ball_detector_training.ipynb`
   - 或手动下载到 models/ 目录

3. **球场关键点检测模型** (`models/keypoints_model.pth`)
   - 训练：使用 `training/tennis_court_keypoints_training.ipynb`
   - 或手动下载到 models/ 目录

## 🔍 故障排除

### Docker 相关问题
- 确保 Docker 和 Docker Compose 已正确安装
- 确保当前用户有 Docker 权限：`sudo usermod -aG docker $USER`

### GUI 显示问题
如果需要显示 OpenCV 窗口，确保：
- 设置了 `DISPLAY` 环境变量
- 允许 X11 转发：`xhost +local:docker`

### 内存问题
- 如果遇到内存不足，可以减少批处理大小或使用更小的模型

## 📝 注意事项

1. 首次构建可能需要较长时间下载依赖
2. 确保有足够的磁盘空间（建议至少 5GB）
3. 模型文件较大，请确保网络连接稳定
4. 生成的视频文件会保存在 `output_videos/` 目录

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目！
