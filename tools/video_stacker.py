import os
from moviepy.editor import VideoFileClip
from moviepy.editor import clips_array
from moviepy.editor import vfx
from tools.generate_id import generate_random_hash

def stack_two_videos(video_path_1, video_path_2, subs=False):
    clip1 = VideoFileClip(video_path_1)
    clip2 = VideoFileClip(video_path_2)

    duration_clip1 = clip1.duration
    duration_clip2 = clip2.duration
    speed_factor = duration_clip1 / duration_clip2
    clip2_resized = clip2.fx(vfx.speedx, 1/speed_factor)

    clip2_resized = clip2_resized.resize(width=clip1.size[0])
    clip2_resized = clip2_resized.without_audio()

    final_clip = clips_array([[clip2_resized], [clip1]])

    unique_id = generate_random_hash()
    media_folder = f"media/adapted_/{unique_id}"
    os.makedirs(media_folder, exist_ok=True)
    output_path = f"{media_folder}/final_video.mp4"
    final_clip.write_videofile(output_path)
    print(f"Видео успешно сохранено в: {output_path}")
    return output_path

if __name__ == '__main__':
        
    video_path_1 = "/Users/maratorozaliev/Desktop/ishowspeed-almost-dies-doing-the-vacuum-challenge-1080-publer.io.mp4"
    video_path_2 = "/Users/maratorozaliev/Desktop/invideo-ai-480 Cosmonaut's Epic Space Adventure! 2024-11-10.mp4"
    output_video = stack_two_videos(video_path_1, video_path_2)