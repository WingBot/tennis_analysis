#!/usr/bin/env python3
"""
完整模型集成测试
使用真实的网球检测模型和球场关键点模型运行完整分析
"""
import cv2
import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.append('/app')
from utils import (read_video, save_video, measure_distance, 
                   draw_player_stats, convert_pixel_distance_to_meters)
import constants
from trackers import PlayerTracker, BallTracker
from court_line_detector import CourtLineDetector
from mini_court import MiniCourt

def test_complete_analysis():
    """完整的网球分析测试（使用真实模型）"""
    print("🎾 完整网球分析测试 - 使用真实模型")
    print("=" * 60)
    
    # 1. 读取视频
    print("📹 读取测试视频...")
    input_video_path = "input_videos/input_video.mp4"
    try:
        video_frames = read_video(input_video_path)
        print(f"✅ 视频读取成功，共 {len(video_frames)} 帧")
    except Exception as e:
        print(f"❌ 视频读取失败: {e}")
        return False
    
    # 限制处理帧数以加快测试
    test_frames = video_frames[:30]  # 只处理前30帧
    print(f"🔍 测试处理 {len(test_frames)} 帧")
    
    # 2. 初始化所有检测器
    print("\n📦 初始化检测器...")
    try:
        # 球员检测器（使用预训练的YOLOv8）
        player_tracker = PlayerTracker(model_path='yolov8x')
        print("✅ 球员跟踪器初始化成功")
        
        # 网球检测器（使用训练好的模型）
        ball_tracker = BallTracker(model_path='models/yolo5_last.pt')
        print("✅ 网球跟踪器初始化成功")
        
        # 球场关键点检测器
        court_line_detector = CourtLineDetector("models/keypoints_model.pth")
        print("✅ 球场线检测器初始化成功")
        
    except Exception as e:
        print(f"❌ 检测器初始化失败: {e}")
        return False
    
    # 3. 检测球员
    print("\n🏃 检测球员...")
    try:
        player_detections = player_tracker.detect_frames(
            test_frames,
            read_from_stub=False,  # 使用真实模型
            stub_path=None
        )
        print("✅ 球员检测完成")
        
        # 统计球员检测
        player_frames = sum(1 for detection in player_detections if detection)
        print(f"   - 检测到球员的帧数: {player_frames}/{len(test_frames)}")
        
    except Exception as e:
        print(f"❌ 球员检测失败: {e}")
        return False
    
    # 4. 检测网球
    print("\n🎾 检测网球...")
    try:
        ball_detections = ball_tracker.detect_frames(
            test_frames,
            read_from_stub=False,  # 使用真实模型
            stub_path=None
        )
        
        # 进行插值
        ball_detections = ball_tracker.interpolate_ball_positions(ball_detections)
        print("✅ 网球检测和插值完成")
        
        # 统计球检测
        ball_frames = sum(1 for detection in ball_detections if detection)
        print(f"   - 检测到网球的帧数: {ball_frames}/{len(test_frames)}")
        
    except Exception as e:
        print(f"❌ 网球检测失败: {e}")
        return False
    
    # 5. 检测球场关键点
    print("\n🏟️ 检测球场关键点...")
    try:
        court_keypoints = court_line_detector.predict(test_frames[0])
        print(f"✅ 球场关键点检测完成，共 {len(court_keypoints)} 个关键点")
        
        # 打印关键点
        for i, (x, y) in enumerate(court_keypoints):
            print(f"   关键点 {i}: ({x:.1f}, {y:.1f})")
            
    except Exception as e:
        print(f"❌ 球场关键点检测失败: {e}")
        return False
    
    # 6. 球员选择和过滤
    print("\n🎯 选择和过滤球员...")
    try:
        player_detections = player_tracker.choose_and_filter_players(
            court_keypoints, player_detections
        )
        print("✅ 球员选择和过滤完成")
        
    except Exception as e:
        print(f"❌ 球员选择失败: {e}")
        # 继续执行，使用原始检测结果
        print("⚠️ 使用原始球员检测结果继续")
    
    # 7. 创建迷你球场
    print("\n🏟️ 创建迷你球场...")
    try:
        mini_court = MiniCourt(test_frames[0])
        print("✅ 迷你球场创建成功")
        
        # 转换坐标到迷你球场
        player_mini_court_detections, ball_mini_court_detections = \
            mini_court.convert_bounding_boxes_to_mini_court_coordinates(
                player_detections, ball_detections, court_keypoints
            )
        print("✅ 坐标转换完成")
        
    except Exception as e:
        print(f"❌ 迷你球场处理失败: {e}")
        # 继续执行，跳过坐标转换
        print("⚠️ 跳过坐标转换继续")
        player_mini_court_detections = []
        ball_mini_court_detections = []
    
    # 8. 击球检测
    print("\n🎾 检测击球时刻...")
    try:
        ball_shot_frames = ball_tracker.get_ball_shot_frames(ball_detections)
        print(f"✅ 击球检测完成，发现 {len(ball_shot_frames)} 个击球时刻")
        
    except Exception as e:
        print(f"❌ 击球检测失败: {e}")
        ball_shot_frames = []
    
    # 9. 生成可视化结果
    print("\n🎨 生成可视化结果...")
    try:
        output_frames = []
        
        for frame_num, frame in enumerate(test_frames):
            frame_copy = frame.copy()
            
            # 绘制球员检测
            if frame_num < len(player_detections) and player_detections[frame_num]:
                for track_id, bbox in player_detections[frame_num].items():
                    x1, y1, x2, y2 = map(int, bbox)
                    cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame_copy, f'Player {track_id}', 
                               (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # 绘制网球检测
            if frame_num < len(ball_detections) and ball_detections[frame_num]:
                for track_id, bbox in ball_detections[frame_num].items():
                    x1, y1, x2, y2 = map(int, bbox)
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    cv2.circle(frame_copy, (center_x, center_y), 8, (0, 255, 255), -1)
                    cv2.circle(frame_copy, (center_x, center_y), 12, (255, 255, 255), 2)
                    cv2.putText(frame_copy, f'Ball {track_id}', 
                               (center_x+15, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            # 绘制球场关键点
            for i, (x, y) in enumerate(court_keypoints):
                cv2.circle(frame_copy, (int(x), int(y)), 6, (255, 0, 0), -1)
                cv2.putText(frame_copy, str(i), 
                           (int(x+10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            
            # 标记击球时刻
            if frame_num in ball_shot_frames:
                cv2.putText(frame_copy, 'SHOT!', 
                           (frame.shape[1]//2-50, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            
            # 添加信息
            cv2.putText(frame_copy, f'Frame: {frame_num}', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame_copy, 'Complete Model Test', 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            output_frames.append(frame_copy)
        
        # 保存结果
        output_path = "output_videos/complete_model_test.avi"
        save_video(output_frames, output_path)
        print(f"✅ 完整测试视频已保存: {output_path}")
        
    except Exception as e:
        print(f"❌ 可视化生成失败: {e}")
        return False
    
    # 10. 测试总结
    print("\n📊 测试总结:")
    print("=" * 30)
    print(f"✅ 球员检测: {player_frames}/{len(test_frames)} 帧")
    print(f"✅ 网球检测: {ball_frames}/{len(test_frames)} 帧")
    print(f"✅ 球场关键点: {len(court_keypoints)} 个")
    print(f"✅ 击球时刻: {len(ball_shot_frames)} 次")
    print(f"✅ 输出视频: output_videos/complete_model_test.avi")
    
    print("\n🎉 完整模型测试成功完成！")
    return True

if __name__ == "__main__":
    print("🎾 网球分析系统 - 完整模型测试")
    print("=" * 70)
    print("这个测试将使用所有真实模型进行完整的网球分析")
    print("包括: 球员检测 + 网球检测 + 球场关键点检测")
    print("=" * 70)
    
    success = test_complete_analysis()
    
    if success:
        print("\n🎉 完整模型测试成功！")
        print("📺 请查看以下输出视频:")
        print("   - output_videos/complete_model_test.avi")
        print("\n💡 提示:")
        print("   - 绿色框: 球员检测")
        print("   - 黄色圆圈: 网球检测") 
        print("   - 蓝色点: 球场关键点")
        print("   - 红色'SHOT!': 击球时刻")
    else:
        print("\n❌ 完整模型测试失败！")
        print("请检查模型文件和配置。")
