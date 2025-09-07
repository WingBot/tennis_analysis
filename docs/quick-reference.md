# 网球分析系统 - 快速参考

## 🚀 快速启动

### 完整分析 (推荐) ✅
```bash
# 进入项目目录
cd /home/czzr/Project/tennis_sys/tennis_analysis

# 运行完整工作版本 (已验证成功)
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python main_working.py
```

**成功标志:** 
- 🎥 处理214帧视频
- 🏟️ 检测14个球场关键点
- 🎾 发现10个击球时刻  
- 📊 平均球速13.0 km/h
- 💾 生成 `output_videos/output_video_complete.avi` (~45MB)

### 快速验证测试
```bash
# 运行验证测试
docker run --rm -v "$PWD":/workspace -w /workspace tennis-analysis:latest python test_validation.py
```

**期望输出:** 生成 `output_videos/model_validation_test.avi` (~3.7MB)

## ⚡ 快速命令

### 环境检查

```bash
docker --version                    # 检查Docker
docker images | grep tennis        # 查看镜像
ls -la input_videos/               # 检查输入文件
```

### 下载模型

```bash
./start.sh                         # 选择选项7
# 或手动下载:
wget -O models/yolov8x.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt
```

### 运行测试

```bash
docker run -it --rm \
  -v $(pwd)/input_videos:/app/input_videos \
  -v $(pwd)/output_videos:/app/output_videos \
  -v $(pwd)/tracker_stubs:/app/tracker_stubs \
  -v $(pwd):/app \
  tennis-analysis:latest python main_test.py
```

### 检查结果

```bash
ls -la output_videos/              # 查看输出文件
ffprobe output_videos/output_video_test.avi  # 视频信息
```

## 🔧 故障排除

| 问题             | 解决方案                           |
| ---------------- | ---------------------------------- |
| Docker镜像不存在 | `./start.sh` → 选择1和4构建镜像 |
| 模型文件缺失     | `./start.sh` → 选择7下载模型    |
| 权限被拒绝       | `sudo chown -R $USER:$USER .`    |
| 内存不足         | 编辑main_test.py减少处理帧数       |
| 磁盘空间不足     | `docker system prune -f`         |

## 📊 成功标志

✅ 程序运行时应显示:

- 🎾 启动网球分析程序...
- ✅ 视频读取完成，共 214 帧
- ✅ 球员检测数据加载完成
- ✅ 球检测数据加载完成
- ✅ 测试视频保存完成

✅ 输出视频应包含:

- 绿色矩形框 (球员)
- 黄色圆点 (网球)
- 帧数显示
- 约9MB大小

## 📁 重要文件

```
tennis_analysis/
├── main.py              # 完整版程序
├── main_test.py         # 测试版程序  
├── start.sh             # 一键脚本
├── input_videos/        # 输入视频
├── output_videos/       # 输出结果
├── models/              # 模型文件
├── tracker_stubs/       # 预处理数据
└── docs/                # 文档目录
    ├── quick-test.sh           # 快速测试脚本
    ├── step-by-step-guide.md   # 详细指南
    └── test-verification-steps.md  # 验证步骤
```

## 🎯 测试流程

1. **环境准备** → 检查Docker和文件
2. **模型下载** → 获取yolov8x.pt
3. **运行测试** → 执行main_test.py
4. **验证结果** → 检查输出视频
5. **查看效果** → 播放检测视频

## 💡 提示

- 首次运行需要下载131MB模型文件
- 测试版本处理50帧约需1-3分钟
- 输出视频可用任何播放器查看
- 成功后可尝试自定义视频文件

---

**快速帮助**: 运行 `bash docs/quick-test.sh` 进行自动化测试
