from utils import (read_video, 
                   save_video,
                   measure_distance,
                   draw_player_stats,
                   convert_pixel_distance_to_meters
                   )
import constants
from trackers import PlayerTracker,BallTracker
# from court_line_detector import CourtLineDetector
from mini_court import MiniCourt
import cv2
import pandas as pd
from copy import deepcopy
import pickle


def main():
    print("🎾 启动网球分析程序...")
    
    # Read Video
    input_video_path = "input_videos/input_video.mp4"
    print(f"📹 读取视频: {input_video_path}")
    video_frames = read_video(input_video_path)
    print(f"✅ 视频读取完成，共 {len(video_frames)} 帧")

    # 使用预处理的检测数据而不是实时检测
    print("📦 加载预处理的检测数据...")
    
    # 加载球员检测数据
    with open("tracker_stubs/player_detections.pkl", "rb") as f:
        player_detections = pickle.load(f)
    print("✅ 球员检测数据加载完成")
    
    # 加载球检测数据
    with open("tracker_stubs/ball_detections.pkl", "rb") as f:
        ball_detections = pickle.load(f)
    print("✅ 球检测数据加载完成")

    # 手动进行球位置插值处理（避免模型加载）
    print("🔄 手动进行球位置插值...")
    
    # 简化的球位置插值
    import pandas as pd
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
    
    # 跳过球场检测，使用默认关键点
    print("⚠️ 跳过球场关键点检测（需要模型文件）")
    # 创建默认关键点（简化处理）
    court_keypoints = [[100, 100], [200, 100], [300, 100], [400, 100],
                       [100, 200], [200, 200], [300, 200], [400, 200],
                       [100, 300], [200, 300], [300, 300], [400, 300],
                       [150, 150], [350, 250]]

    # 创建PlayerTracker实例用于后续处理（避免模型加载）
    # player_tracker = PlayerTracker(model_path=None)  # 跳过PlayerTracker初始化
    
    # choose players (简化处理)
    print("🏃 处理球员选择...")
    # player_detections = player_tracker.choose_and_filter_players(court_keypoints, player_detections)

    # MiniCourt
    print("🏟️ 创建迷你球场...")
    mini_court = MiniCourt(video_frames[0]) 

    # 简化击球检测（避免使用模型）
    print("🎾 简化击球检测...")
    # 假设每10帧有一次击球
    ball_shot_frames = [i for i in range(0, len(video_frames), 10)]
    print(f"✅ 模拟发现 {len(ball_shot_frames)} 个击球时刻")

    # 跳过迷你球场坐标转换（需要复杂的几何计算）
    print("📍 跳过坐标转换到迷你球场...")
    player_mini_court_detections = []
    ball_mini_court_detections = []

    # 简化统计数据处理
    print("📊 处理统计数据...")
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

    # 简化处理前几帧
    print("🎬 处理视频帧...")
    for frame_num, frame in enumerate(video_frames[:50]):  # 只处理前50帧进行测试
        
        # Draw player detections
        if frame_num < len(player_detections):
            for track_id, bbox in player_detections[frame_num].items():
                frame = cv2.rectangle(frame, 
                                    (int(bbox[0]), int(bbox[1])),
                                    (int(bbox[2]), int(bbox[3])),
                                    (0, 255, 0), 2)
                # 添加跟踪ID
                cv2.putText(frame, f'Player {track_id}', 
                           (int(bbox[0]), int(bbox[1])-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Draw ball detections
        if frame_num < len(ball_detections) and ball_detections[frame_num] and 1 in ball_detections[frame_num]:
            bbox = ball_detections[frame_num][1]
            center_x = int((bbox[0] + bbox[2]) / 2)
            center_y = int((bbox[1] + bbox[3]) / 2)
            frame = cv2.circle(frame, (center_x, center_y), 10, (0, 255, 255), -1)

        # 添加帧数信息
        cv2.putText(frame, f'Frame: {frame_num}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    print("💾 保存输出视频...")
    # Save video
    output_video_frames = video_frames[:50]  # 只保存前50帧
    save_video(output_video_frames, "output_videos/output_video_test.avi")
    print("✅ 测试视频保存完成: output_videos/output_video_test.avi")

if __name__ == '__main__':
    main()
