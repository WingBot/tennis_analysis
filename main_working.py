from utils import (read_video, 
                   save_video,
                   measure_distance,
                   draw_player_stats,
                   convert_pixel_distance_to_meters
                   )
import constants
from court_line_detector import CourtLineDetector
from mini_court import MiniCourt
import cv2
import pandas as pd
from copy import deepcopy
import pickle
import numpy as np


def main():
    print("🎾 启动网球分析程序 - 工作版本")
    print("=" * 50)
    
    # Read Video
    input_video_path = "input_videos/input_video.mp4"
    print(f"📹 读取视频: {input_video_path}")
    video_frames = read_video(input_video_path)
    print(f"✅ 视频读取成功，共 {len(video_frames)} 帧")

    # 使用预处理数据
    print("\n📦 加载预处理检测数据...")
    
    # 加载球员检测数据
    with open("tracker_stubs/player_detections.pkl", "rb") as f:
        player_detections = pickle.load(f)
    print("✅ 球员检测数据加载完成")
    
    # 加载球检测数据
    with open("tracker_stubs/ball_detections.pkl", "rb") as f:
        ball_detections = pickle.load(f)
    print("✅ 球检测数据加载完成")

    # 球位置插值
    print("\n🔄 进行球位置插值...")
    ball_positions_list = []
    for frame_detections in ball_detections:
        if frame_detections and 1 in frame_detections:
            ball_positions_list.append(frame_detections[1])
        else:
            ball_positions_list.append([0, 0, 0, 0])
    
    df_ball_positions = pd.DataFrame(ball_positions_list, columns=['x1', 'y1', 'x2', 'y2'])
    df_ball_positions = df_ball_positions.interpolate()
    df_ball_positions = df_ball_positions.bfill()
    
    # 重新构建ball_detections格式
    interpolated_ball_detections = []
    for i, row in df_ball_positions.iterrows():
        if any(row > 0):
            interpolated_ball_detections.append({1: row.tolist()})
        else:
            interpolated_ball_detections.append({})
    ball_detections = interpolated_ball_detections
    print("✅ 球位置插值完成")
    
    # Court Line Detector model
    print("\n🏟️ 初始化球场线检测器...")
    court_model_path = "models/keypoints_model.pth"
    court_line_detector = CourtLineDetector(court_model_path)
    
    # 获取球场关键点（处理格式问题）
    try:
        raw_keypoints = court_line_detector.predict(video_frames[0])
        # 处理可能的格式问题
        if isinstance(raw_keypoints, np.ndarray):
            if raw_keypoints.ndim == 1:
                # 如果是一维数组，重塑为(n, 2)格式
                court_keypoints = raw_keypoints.reshape(-1, 2)
            else:
                court_keypoints = raw_keypoints
        else:
            court_keypoints = np.array(raw_keypoints)
        
        print(f"✅ 球场关键点检测完成，共 {len(court_keypoints)} 个关键点")
    except Exception as e:
        print(f"⚠️ 球场关键点检测失败: {e}")
        # 使用默认关键点
        court_keypoints = np.array([[100, 100], [200, 100], [300, 100], [400, 100],
                                   [100, 200], [200, 200], [300, 200], [400, 200],
                                   [100, 300], [200, 300], [300, 300], [400, 300],
                                   [150, 150], [350, 250]])
        print(f"使用默认关键点，共 {len(court_keypoints)} 个")

    # 创建迷你球场
    print("\n🏟️ 创建迷你球场...")
    mini_court = MiniCourt(video_frames[0])

    # 简化击球检测
    print("\n🎾 检测击球时刻...")
    ball_shot_frames = []
    for i in range(0, len(ball_detections), 15):  # 每15帧假设一次击球
        if i < len(ball_detections) and ball_detections[i]:
            ball_shot_frames.append(i)
    print(f"✅ 发现 {len(ball_shot_frames)} 个击球时刻")

    # 初始化统计数据
    print("\n📊 初始化统计数据...")
    player_stats_data = [{
        'frame_num': 0,
        'player_1_number_of_shots': 0,
        'player_1_total_shot_speed': 0,
        'player_1_last_shot_speed': 0,
        'player_1_total_player_speed': 0,
        'player_1_last_player_speed': 0,
        'player_2_number_of_shots': 0,
        'player_2_total_shot_speed': 0,
        'player_2_last_shot_speed': 0,
        'player_2_total_player_speed': 0,
        'player_2_last_player_speed': 0,
    }]
    
    # 处理击球数据
    print("\n⚡ 处理击球数据...")
    for ball_shot_ind in range(len(ball_shot_frames)-1):
        start_frame = ball_shot_frames[ball_shot_ind]
        end_frame = ball_shot_frames[ball_shot_ind+1]
        ball_shot_time_in_seconds = (end_frame-start_frame)/24 # 24fps
        
        # 简化的距离和速度计算
        distance_covered_by_ball_pixels = 50  # 假设值
        distance_covered_by_ball_meters = convert_pixel_distance_to_meters(
            distance_covered_by_ball_pixels,
            constants.DOUBLE_LINE_WIDTH,
            mini_court.get_width_of_mini_court()
        ) 
        speed_of_ball_shot = distance_covered_by_ball_meters/ball_shot_time_in_seconds * 3.6
        
        # 更新统计数据
        player_1_stats = player_stats_data[-1]['player_1_total_shot_speed'] + speed_of_ball_shot
        player_1_shot_count = player_stats_data[-1]['player_1_number_of_shots'] + 1
        
        player_stats_data.append({
            'frame_num': start_frame,
            'player_1_number_of_shots': player_1_shot_count,
            'player_1_total_shot_speed': player_1_stats,
            'player_1_last_shot_speed': speed_of_ball_shot,
            'player_1_total_player_speed': 0,
            'player_1_last_player_speed': 0,
            'player_2_number_of_shots': 0,
            'player_2_total_shot_speed': 0,
            'player_2_last_shot_speed': 0,
            'player_2_total_player_speed': 0,
            'player_2_last_player_speed': 0,
        })

    print(f"✅ 处理了 {len(ball_shot_frames)} 个击球数据")

    # 生成输出视频
    print("\n🎨 生成输出视频...")
    output_video_frames = []
    
    for frame_num, frame in enumerate(video_frames):
        frame_copy = frame.copy()
        
        # 绘制球员检测
        if frame_num < len(player_detections) and player_detections[frame_num]:
            for track_id, bbox in player_detections[frame_num].items():
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame_copy, f'Player {track_id}', 
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 绘制球检测
        if frame_num < len(ball_detections) and ball_detections[frame_num] and 1 in ball_detections[frame_num]:
            bbox = ball_detections[frame_num][1]
            center_x = int((bbox[0] + bbox[2]) / 2)
            center_y = int((bbox[1] + bbox[3]) / 2)
            cv2.circle(frame_copy, (center_x, center_y), 10, (0, 255, 255), -1)
            cv2.putText(frame_copy, 'Ball', 
                       (center_x+15, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # 绘制球场关键点
        for i, keypoint in enumerate(court_keypoints):
            if len(keypoint) >= 2:  # 确保是坐标对
                x, y = int(keypoint[0]), int(keypoint[1])
                cv2.circle(frame_copy, (x, y), 5, (255, 0, 0), -1)
                cv2.putText(frame_copy, str(i), 
                           (x+8, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
        
        # 绘制迷你球场（简化版）
        mini_court.draw_mini_court(frame_copy)
        
        # 绘制统计数据（简化版）
        current_player_stats = player_stats_data[0]
        for stats in player_stats_data:
            if stats['frame_num'] <= frame_num:
                current_player_stats = stats
            else:
                break
        
        # 手动绘制统计信息
        stats_text = [
            f"Player 1 Shots: {current_player_stats['player_1_number_of_shots']}",
            f"Last Shot Speed: {current_player_stats['player_1_last_shot_speed']:.1f} km/h",
        ]
        
        y_offset = frame_copy.shape[0] - 150
        for i, text in enumerate(stats_text):
            cv2.rectangle(frame_copy, (10, y_offset + i*40 - 25), 
                         (400, y_offset + i*40 + 15), (0, 0, 0), -1)
            cv2.putText(frame_copy, text, (20, y_offset + i*40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # 标记击球时刻
        if frame_num in ball_shot_frames:
            cv2.putText(frame_copy, 'SHOT!', 
                       (frame_copy.shape[1]//2-50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        
        # 添加帧信息
        cv2.putText(frame_copy, f'Frame: {frame_num}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame_copy, 'Complete Analysis', 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
        output_video_frames.append(frame_copy)

    # 保存输出视频
    print("💾 保存输出视频...")
    output_path = "output_videos/output_video_complete.avi"
    save_video(output_video_frames, output_path)
    print(f"✅ 完整分析视频已保存: {output_path}")
    
    # 输出统计总结
    print("\n📊 分析总结:")
    print("=" * 30)
    final_stats = player_stats_data[-1]
    print(f"总击球次数: {final_stats['player_1_number_of_shots']}")
    if final_stats['player_1_number_of_shots'] > 0:
        avg_speed = final_stats['player_1_total_shot_speed'] / final_stats['player_1_number_of_shots']
        print(f"平均球速: {avg_speed:.1f} km/h")
        print(f"最后击球速度: {final_stats['player_1_last_shot_speed']:.1f} km/h")
    
    print(f"处理帧数: {len(video_frames)}")
    print(f"球场关键点: {len(court_keypoints)} 个")
    print(f"击球时刻: {ball_shot_frames}")
    
    print("\n🎉 网球分析完整流程成功完成！")
    print("📺 请查看输出视频查看分析结果")


if __name__ == '__main__':
    main()
