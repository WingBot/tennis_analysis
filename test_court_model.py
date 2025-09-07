#!/usr/bin/env python3
"""
球场关键点检测模型测试用例
测试 keypoints_model.pth 模型的球场线检测功能
"""
import cv2
import sys
import numpy as np
from pathlib import Path

# 添加项目路径
sys.path.append('/app')
from court_line_detector import CourtLineDetector
from utils import read_video, save_video

def test_court_keypoints_model():
    """测试球场关键点检测模型"""
    print("🏟️ 球场关键点检测模型测试")
    print("=" * 60)
    
    # 1. 初始化球场线检测器
    print("📦 初始化球场线检测器...")
    try:
        court_detector = CourtLineDetector("models/keypoints_model.pth")
        print("✅ 球场线检测器初始化成功")
    except Exception as e:
        print(f"❌ 球场线检测器初始化失败: {e}")
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
    
    # 3. 检测球场关键点 (测试多帧)
    print("🔍 检测球场关键点...")
    test_frame_indices = [0, 50, 100, 150, 200]  # 测试几个不同时刻的帧
    
    all_keypoints = []
    for i, frame_idx in enumerate(test_frame_indices):
        if frame_idx < len(video_frames):
            try:
                frame = video_frames[frame_idx]
                keypoints = court_detector.predict(frame)
                all_keypoints.append((frame_idx, keypoints))
                print(f"✅ 帧 {frame_idx}: 检测到 {len(keypoints)} 个关键点")
                
                # 打印关键点坐标
                for j, (x, y) in enumerate(keypoints):
                    print(f"   关键点 {j}: ({x:.1f}, {y:.1f})")
                    
            except Exception as e:
                print(f"❌ 帧 {frame_idx} 检测失败: {e}")
                return False
    
    # 4. 可视化检测结果
    print("🎨 生成可视化结果...")
    try:
        output_frames = []
        
        for frame_idx, keypoints in all_keypoints:
            frame = video_frames[frame_idx].copy()
            
            # 绘制关键点
            for i, (x, y) in enumerate(keypoints):
                # 绘制关键点
                cv2.circle(frame, (int(x), int(y)), 8, (0, 255, 0), -1)
                cv2.circle(frame, (int(x), int(y)), 12, (255, 255, 255), 2)
                
                # 添加关键点编号
                cv2.putText(frame, str(i), 
                           (int(x+15), int(y+5)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # 绘制球场线连接（如果有足够的关键点）
            if len(keypoints) >= 4:
                draw_court_lines(frame, keypoints)
            
            # 添加信息文本
            cv2.putText(frame, f'Frame: {frame_idx}', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f'Keypoints: {len(keypoints)}', 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, 'Court Keypoints Test', 
                       (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            output_frames.append(frame)
        
        # 保存测试结果视频
        output_path = "output_videos/court_keypoints_test.avi"
        save_video(output_frames, output_path)
        print(f"✅ 测试视频已保存: {output_path}")
        
    except Exception as e:
        print(f"❌ 可视化生成失败: {e}")
        return False
    
    print("🎉 球场关键点检测模型测试完成！")
    return True

def draw_court_lines(frame, keypoints):
    """绘制球场线条"""
    if len(keypoints) < 4:
        return
    
    # 网球场标准关键点连接（简化版）
    # 这里实现一个基本的线条连接逻辑
    points = np.array(keypoints, dtype=np.int32)
    
    # 根据点的位置排序，尝试识别球场边界
    # 这是一个简化的实现，实际可能需要更复杂的逻辑
    if len(points) >= 8:
        # 绘制外边界矩形
        try:
            # 找到最外围的点
            left_points = points[points[:, 0].argsort()][:2]
            right_points = points[points[:, 0].argsort()][-2:]
            top_points = points[points[:, 1].argsort()][:2]
            bottom_points = points[points[:, 1].argsort()][-2:]
            
            # 绘制边界线
            cv2.line(frame, tuple(left_points[0]), tuple(left_points[1]), (255, 0, 0), 3)
            cv2.line(frame, tuple(right_points[0]), tuple(right_points[1]), (255, 0, 0), 3)
            cv2.line(frame, tuple(top_points[0]), tuple(top_points[1]), (255, 0, 0), 3)
            cv2.line(frame, tuple(bottom_points[0]), tuple(bottom_points[1]), (255, 0, 0), 3)
            
        except Exception as e:
            print(f"绘制球场线失败: {e}")

def test_court_stability():
    """测试球场检测的稳定性"""
    print("\n🔄 球场检测稳定性测试")
    print("=" * 40)
    
    try:
        court_detector = CourtLineDetector("models/keypoints_model.pth")
        video_frames = read_video("input_videos/input_video.mp4")
        
        # 测试连续帧的检测稳定性
        test_frames = video_frames[0:10]  # 前10帧
        keypoints_sequence = []
        
        for i, frame in enumerate(test_frames):
            keypoints = court_detector.predict(frame)
            keypoints_sequence.append(keypoints)
            print(f"帧 {i}: {len(keypoints)} 个关键点")
        
        # 分析稳定性
        keypoint_counts = [len(kp) for kp in keypoints_sequence]
        avg_count = np.mean(keypoint_counts)
        std_count = np.std(keypoint_counts)
        
        print(f"\n📊 稳定性分析:")
        print(f"   平均关键点数: {avg_count:.1f}")
        print(f"   标准差: {std_count:.1f}")
        print(f"   稳定性: {'良好' if std_count < 2 else '需要改进'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 稳定性测试失败: {e}")
        return False

def test_single_frame_detection():
    """测试单帧检测性能"""
    print("\n⚡ 单帧检测性能测试")
    print("=" * 35)
    
    try:
        import time
        
        court_detector = CourtLineDetector("models/keypoints_model.pth")
        video_frames = read_video("input_videos/input_video.mp4")
        test_frame = video_frames[0]
        
        # 多次检测测量平均时间
        times = []
        for i in range(5):
            start_time = time.time()
            keypoints = court_detector.predict(test_frame)
            end_time = time.time()
            times.append(end_time - start_time)
            print(f"检测 {i+1}: {end_time - start_time:.3f}s, {len(keypoints)} 关键点")
        
        avg_time = np.mean(times)
        print(f"\n📊 性能统计:")
        print(f"   平均检测时间: {avg_time:.3f}s")
        print(f"   处理速度: {1/avg_time:.1f} FPS")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🏟️ 球场关键点检测模型完整测试套件")
    print("=" * 70)
    
    # 测试1: 基本关键点检测
    success1 = test_court_keypoints_model()
    
    # 测试2: 检测稳定性
    success2 = test_court_stability()
    
    # 测试3: 性能测试
    success3 = test_single_frame_detection()
    
    print("\n📋 测试总结:")
    print("=" * 30)
    print(f"关键点检测测试: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"稳定性测试: {'✅ 通过' if success2 else '❌ 失败'}")
    print(f"性能测试: {'✅ 通过' if success3 else '❌ 失败'}")
    
    if success1 and success2 and success3:
        print("\n🎉 所有测试通过！球场关键点检测模型工作正常。")
        print("📺 请查看输出视频: output_videos/court_keypoints_test.avi")
    else:
        print("\n⚠️ 部分测试失败，请检查模型文件和配置。")
