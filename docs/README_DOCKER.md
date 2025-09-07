# 网球分析项目 Docker 开发环境

## 项目概述

这是一个基于深度学习的网球视频分析项目，可以检测球员、网球和球场线，并提供比赛统计分析。

## 🏗️ 分阶段构建策略

为了解决依赖安装问题和构建失败的情况，本项目采用分阶段构建策略：

1. **基础镜像构建**：只包含系统依赖，快速构建
2. **开发环境测试**：在容器内逐步安装和测试 Python 依赖
3. **最终镜像生成**：基于验证的依赖列表生成生产镜像

## 🚀 快速开始

### 第一阶段：构建基础镜像

```bash
# 使用一键启动脚本
./start.sh
# 选择选项 1：构建基础镜像

# 或直接执行
./scripts/build-base.sh
```

### 第二阶段：开发环境测试

```bash
# 启动开发环境
./start.sh
# 选择选项 2：启动开发环境

# 或直接执行
./scripts/run-dev-base.sh
```

在开发环境容器内执行：

```bash
# 分阶段安装依赖
./scripts/install-deps.sh

# 测试环境
./scripts/test-env.sh
```

### 第三阶段：生成最终镜像

```bash
# 在主机上执行
./start.sh
# 选择选项 4：生成最终生产镜像

# 或直接执行
./scripts/build-final.sh
```

## 📋 可用脚本说明

### 构建相关脚本

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `scripts/build-base.sh` | 构建基础镜像 | 首次设置或重新开始 |
| `scripts/run-dev-base.sh` | 启动开发环境 | 依赖测试和开发 |
| `scripts/install-deps.sh` | 分阶段安装依赖 | 在开发容器内执行 |
| `scripts/test-env.sh` | 测试环境和依赖 | 验证安装结果 |
| `scripts/build-final.sh` | 生成生产镜像 | 完成开发后固化环境 |

### 运行相关脚本

| 脚本 | 功能 | 前提条件 |
|------|------|----------|
| `scripts/run-main.sh` | 运行主程序 | 需要生产镜像 |
| `scripts/download-models.sh` | 下载模型 | 任何时候 |
| `scripts/cleanup.sh` | 清理环境 | 任何时候 |

### 一键启动脚本

```bash
./start.sh
```

提供完整的菜单式操作界面。

## 📁 项目结构

```
tennis_analysis/
├── docker/                    # Docker 配置文件目录
│   ├── Dockerfile.base        # 基础镜像 Dockerfile
│   ├── Dockerfile.final       # 最终镜像 Dockerfile（自动生成）
│   ├── docker-compose.dev.yml # 开发环境 Compose 配置
│   └── .dockerignore          # Docker 忽略文件
├── scripts/                   # 构建和运行脚本
│   ├── build-base.sh         # 构建基础镜像
│   ├── run-dev-base.sh       # 启动开发环境
│   ├── install-deps.sh       # 安装依赖（容器内执行）
│   ├── test-env.sh           # 测试环境（容器内执行）
│   ├── build-final.sh        # 构建最终镜像
│   ├── run-main.sh           # 运行主程序
│   ├── download-models.sh    # 下载模型
│   └── cleanup.sh            # 清理环境
├── requirements-*.txt         # 分级依赖文件
├── main.py                   # 主程序
├── start.sh                  # 一键启动脚本
└── ...                       # 其他项目文件
```

## 📦 依赖管理

### 分级依赖文件

- `requirements-base.txt`：基础核心依赖（NumPy、OpenCV 等）
- `requirements-ml.txt`：机器学习依赖（PyTorch、YOLO 等）
- `requirements-data.txt`：数据处理依赖（Pandas、Scikit-learn 等）
- `requirements-dev.txt`：开发工具依赖（Jupyter 等）
- `requirements-final.txt`：最终验证的完整依赖列表（自动生成）

### 安装策略

依赖安装采用渐进式策略，即使某个阶段失败也能继续安装其他依赖，确保核心功能可用。

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

## 🔧 开发工作流

### 完整开发流程

1. **初始化环境**
   ```bash
   ./start.sh  # 选择 1：构建基础镜像
   ```

2. **进入开发环境**
   ```bash
   ./start.sh  # 选择 2：启动开发环境
   ```

3. **在容器内安装和测试依赖**
   ```bash
   ./scripts/install-deps.sh
   ./scripts/test-env.sh
   ```

4. **开发和调试**
   - 修改代码
   - 测试功能
   - 调试问题

5. **生成生产镜像**
   ```bash
   exit  # 退出容器
   ./start.sh  # 选择 4：生成最终生产镜像
   ```

6. **运行生产程序**
   ```bash
   ./start.sh  # 选择 5：运行网球分析
   ```

### Jupyter 开发

```bash
./start.sh  # 选择 6：启动 Jupyter Lab
```

然后访问 `http://localhost:8888`

## 🔍 故障排除

### 基础镜像构建失败
- 检查 Docker 服务是否运行
- 检查网络连接
- 清理 Docker 缓存：`docker system prune -a`

### 依赖安装失败
- 在开发环境中逐个安装：`pip install package_name`
- 检查 Python 版本兼容性
- 查看详细错误信息

### 内存不足
- 关闭其他应用程序
- 增加 Docker 内存限制
- 使用更小的模型

### GPU 支持
编辑 `docker/docker-compose.dev.yml`，取消 GPU 配置的注释。

## 📊 镜像大小优化

- 基础镜像：~800MB（仅系统依赖）
- 完整镜像：~2-3GB（包含所有 Python 依赖）
- 使用多阶段构建减少最终镜像大小

## 🎯 生产部署

生成的最终镜像可以直接用于生产部署：

```bash
docker run -it \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/models:/app/models \
  tennis-analysis:latest
```

## 📝 注意事项

1. **磁盘空间**：确保至少有 5GB 可用空间
2. **网络连接**：依赖下载需要稳定的网络
3. **系统兼容性**：支持 x86_64 Linux 系统
4. **模型文件**：确保模型文件放置在正确位置

## 🆘 获取帮助

1. 查看构建日志
2. 检查脚本输出信息
3. 使用 `./start.sh` 选项 9 查看镜像状态
4. 参考项目 Issue 和文档

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目的 Docker 化部署！
