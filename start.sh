#!/bin/bash

# 一键启动脚本 - 分阶段构建版本
# 作者: GitHub Copilot

echo "🎾 网球分析项目 - 分阶段构建"
echo "================================"

# 显示菜单
echo ""
echo "🏗️  构建阶段："
echo "1) 构建基础镜像（快速，仅系统依赖）"
echo "2) 启动开发环境（测试依赖安装）"
echo "3) 安装和测试依赖"
echo "4) 生成最终生产镜像"
echo ""
echo "🚀 使用阶段："
echo "5) 运行网球分析（需要先完成构建）"
echo "6) 启动 Jupyter Lab"
echo "7) 下载模型文件"
echo ""
echo "🧹 维护阶段："
echo "8) 清理环境"
echo "9) 查看镜像状态"
echo "0) 退出"

read -p "请输入选项 (0-9): " choice

case $choice in
    1)
        echo "🔨 构建基础镜像..."
        ./scripts/build-base.sh
        ;;
    2)
        echo "🔧 启动开发环境..."
        ./scripts/run-dev-base.sh
        ;;
    3)
        echo "� 请在开发环境容器内执行："
        echo "   ./scripts/install-deps.sh"
        echo "   ./scripts/test-env.sh"
        echo ""
        echo "验证成功后可以执行选项 4 生成最终镜像"
        ;;
    4)
        echo "🎯 生成最终生产镜像..."
        ./scripts/build-final.sh
        ;;
    5)
        echo "� 运行网球分析..."
        if docker images | grep -q "tennis-analysis.*latest"; then
            ./scripts/run-main.sh
        else
            echo "❌ 未找到生产镜像，请先完成构建流程（选项 1-4）"
        fi
        ;;
    6)
        echo "📚 启动 Jupyter Lab..."
        cd docker
        docker-compose -f docker-compose.dev.yml up -d tennis-jupyter
        echo "🌐 访问 http://localhost:8888"
        ;;
    7)
        echo "📥 下载模型文件..."
        ./scripts/download-models.sh
        ;;
    8)
        echo "🧹 清理环境..."
        ./scripts/cleanup.sh
        ;;
    9)
        echo "� 查看镜像状态..."
        echo "基础镜像："
        docker images | grep tennis-analysis-base || echo "  未构建"
        echo "生产镜像："
        docker images | grep "tennis-analysis.*latest" || echo "  未构建"
        echo "运行中的容器："
        docker ps | grep tennis || echo "  无"
        ;;
    0)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选项，请重新运行脚本"
        exit 1
        ;;
esac
