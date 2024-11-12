from tools.video_stacker import stack_two_videos

if __name__ == '__main__':
    video_path_1 = "/Users/maratorozaliev/Desktop/ishowspeed-almost-dies-doing-the-vacuum-challenge-1080-publer.io.mp4"
    video_path_2 = "/Users/maratorozaliev/Desktop/invideo-ai-480 Cosmonaut's Epic Space Adventure! 2024-11-10.mp4"
    output_video = stack_two_videos(video_path_1, video_path_2)
    print(output_video)