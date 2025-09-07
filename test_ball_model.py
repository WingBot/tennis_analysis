#!/usr/bin/env python3
"""
网球检测模型测试用例
测试 yolo5_last.pt 模型的球检测功能
"""
import cv2
import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.append('/app')
from trackers import BallTracker
from utils import read_video, save_video

def test_ball_detection_model():
    """测试网球检测模型"""
    print("🎾 网球检测模型测试")
    print("=" * 50)
    
    # 1. 初始化球跟踪器
    print("📦 初始化球跟踪器...")
    try:
        ball_tracker = BallTracker(model_path='models/yolo5_last.pt')
        print("✅ 球跟踪器初始化成功")
    except Exception as e:
        print(f"❌ 球跟踪器初始化失败: {e}")
        return False
    
    # 2. 读取测试视频
    print("📹 读取测试视频...")
    input_video_path = "input_videos/input_video.mp4"
    try:
        video_frames = read_video(input_video_path)
        print(f"✅ 视频读取成功，共 {len(video_frames)} 帧")
    except Exception as e:
        print(f"❌ 视频读取失败: {e}")
        return False
    
    # 3. 进行球检测 (只检测前20帧)
    print("🔍 进行球检测...")
    test_frames = video_frames[:20]
    try:
        ball_detections = ball_tracker.detect_frames(
            test_frames,
            read_from_stub=False,  # 强制使用模型
            stub_path=None
        )
        print("✅ 球检测完成")
        
        # 统计检测结果
        detected_frames = sum(1 for detection in ball_detections if detection)
        print(f"📊 检测统计:")
        print(f"   - 总帧数: {len(test_frames)}")
        print(f"   - 检测到球的帧数: {detected_frames}")
        print(f"   - 检测率: {detected_frames/len(test_frames)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ 球检测失败: {e}")
        return False
    
    # 4. 可视化检测结果
    print("🎨 生成可视化结果...")
    try:
        output_frames = []
        for frame_num, (frame, detections) in enumerate(zip(test_frames, ball_detections)):
            frame_copy = frame.copy()
            
            # 绘制检测框
            if detections:
                for track_id, bbox in detections.items():
                    x1, y1, x2, y2 = map(int, bbox)
                    # 绘制球的边界框
                    cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 255), 2)
                    # 绘制中心点
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    cv2.circle(frame_copy, (center_x, center_y), 5, (0, 0, 255), -1)
                    # 添加标签
                    cv2.putText(frame_copy, f'Ball {track_id}', 
                               (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # 添加帧信息
            cv2.putText(frame_copy, f'Frame: {frame_num}', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame_copy, f'Ball Model Test', 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            output_frames.append(frame_copy)
        
        # 保存测试结果视频
        output_path = "output_videos/ball_detection_test.avi"
        save_video(output_frames, output_path)
        print(f"✅ 测试视频已保存: {output_path}")
        
    except Exception as e:
        print(f"❌ 可视化生成失败: {e}")
        return False
    
    print("🎉 网球检测模型测试完成！")
    return True

def test_ball_interpolation():
    """测试球位置插值功能"""
    print("\n🔄 球位置插值测试")
    print("=" * 30)
    
    try:
        ball_tracker = BallTracker(model_path='models/yolo5_last.pt')
        
        # 创建模拟检测数据（有间隔的检测）
        mock_detections = [
            {1: [100, 100, 120, 120]},  # 第0帧
            {},                         # 第1帧 (缺失)
            {},                         # 第2帧 (缺失)
            {1: [150, 150, 170, 170]},  # 第3帧
            {},                         # 第4帧 (缺失)
            {1: [200, 200, 220, 220]},  # 第5帧
        ]
        
        print("📊 插值前检测数据:")
        for i, detection in enumerate(mock_detections):
            status = "有检测" if detection else "无检测"
            print(f"   帧 {i}: {status}")
        
        # 进行插值
        interpolated = ball_tracker.interpolate_ball_positions(mock_detections)
        
        print("📊 插值后检测数据:")
        for i, detection in enumerate(interpolated):
            if detection and 1 in detection:
                x1, y1, x2, y2 = detection[1]
                print(f"   帧 {i}: [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]")
            else:
                print(f"   帧 {i}: 无数据")
        
        print("✅ 球位置插值测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 插值测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🎾 网球检测模型完整测试套件")
    print("=" * 60)
    
    # 测试1: 基本球检测
    success1 = test_ball_detection_model()
    
    # 测试2: 插值功能
    success2 = test_ball_interpolation()
    
    print("\n📋 测试总结:")
    print("=" * 30)
    print(f"球检测模型测试: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"插值功能测试: {'✅ 通过' if success2 else '❌ 失败'}")
    
    if success1 and success2:
        print("\n🎉 所有测试通过！网球检测模型工作正常。")
        print("📺 请查看输出视频: output_videos/ball_detection_test.avi")
    else:
        print("\n⚠️ 部分测试失败，请检查模型文件和配置。")
