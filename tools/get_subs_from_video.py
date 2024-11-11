import moviepy.editor as mp
import whisper
import pysrt
import os
from tools.generate_id import generate_random_hash

def extract_audio_from_video(video_path):
    video = mp.VideoFileClip(video_path)
    audio_path = "audio.wav"
    video.audio.write_audiofile(audio_path)
    return audio_path

def recognize_audio_with_whisper(audio_path):
    model = whisper.load_model("large")
    result = model.transcribe(audio_path, word_timestamps=True)

    if os.path.exists(audio_path):
        os.remove(audio_path)
        print("Audio file deleted successfully.")
    else:
        print("Audio file not found.")

    return result['segments']

def create_srt_file(segments, srt_file_path):
    subs = pysrt.SubRipFile()

    for i, segment in enumerate(segments):
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']

        # Преобразуем время в формат SRT (чч:мм:сс,мс)
        start = pysrt.SubRipTime(seconds=start_time)
        end = pysrt.SubRipTime(seconds=end_time)

        # Создаем субтитр
        sub = pysrt.SubRipItem(index=i + 1, start=start, end=end, text=text)
        subs.append(sub)

    # Сохраняем в файл
    subs.save(srt_file_path)
    print(f"SRT file saved to {srt_file_path}")

def get_subs_from_video(video_path):
    audio_path = extract_audio_from_video(video_path)
    segments = recognize_audio_with_whisper(audio_path)
    if not segments:
        print("No speech detected.")
        return


    unique_id = generate_random_hash()
    media_folder = f"media/{unique_id}"
    os.makedirs(media_folder, exist_ok=True)
    srt_file_path = media_folder + "/subs.str"
    create_srt_file(segments, srt_file_path)

if __name__ == '__main__':
    video_path = "/Users/maratorozaliev/Desktop/IMG_0057.MOV"
    get_subs_from_video(video_path)
