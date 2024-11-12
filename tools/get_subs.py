import whisper 
import numpy as np
import datetime
import os
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import cv2
from tools.generate_id import generate_random_hash

def get_video_resolution(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Не удалось открыть видеофайл")
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return (width, height)

def extract_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    wav_path = video_path.rsplit('.', 1)[0] + '.wav'
    audio.write_audiofile(wav_path, codec='pcm_s16le')
    return wav_path

def convert_audio_to_srt(audio_path, task = "translate"):
    model = whisper.load_model("large")
    result = model.transcribe(audio_path, word_timestamps=True, task=task)
    words = result['segments'][0]['words']
    srt_filepath = audio_path.rsplit('.', 1)[0] + '.srt'
    generate_srt(words, filename = srt_filepath)

    os.remove(audio_path)
    return srt_filepath

def convert_seconds_to_srt_time(seconds):
    """Convert seconds to SRT time format: HH:MM:SS,MS"""
    td = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(int(td.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds = int(seconds)
    milliseconds = int((td.total_seconds() - int(td.total_seconds())) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_srt(subtitles, filename="subtitles.srt"):
    with open(filename, 'w') as file:
        for subtitle in subtitles:
            start_time = float(subtitle['start'])
            end_time = float(subtitle['end'])
            sentence = subtitle['word']
            start_time_srt = convert_seconds_to_srt_time(start_time)
            end_time_srt = convert_seconds_to_srt_time(end_time)
            file.write(f"{start_time_srt} --> {end_time_srt}\n")
            file.write(f"{sentence}\n\n")

def str_rewriter_by_words(input_file_path = '', words = 5):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    global_counter = 1
    result = []
    current_subtitle = ""
    start_time_stamp = ""
    counter = 0
    
    for line in content:
        line = line.strip()
        
        if "-->" in line:
            if not start_time_stamp:
                start_time_stamp = line.split(' ')[0]
            last_time_stamp = line.split(' ')[2]
        elif line:
            counter += 1
            if current_subtitle:
                current_subtitle += " " + line
            else:
                current_subtitle = line
            if counter == words:
                counter = 0
                result.append(str(global_counter))
                global_counter += 1
                result.append(start_time_stamp + " --> " + last_time_stamp)
                result.append(current_subtitle)
                result.append('')
                current_subtitle = ""
                start_time_stamp = ""
    
    if current_subtitle:
        result.append(str(global_counter))
        result.append(start_time_stamp + " --> " + last_time_stamp)
        result.append(current_subtitle)
    
    base_name = os.path.splitext(input_file_path)[0]
    new_srt_path = base_name + '_changed.srt'
    
    with open(new_srt_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(result))

    os.remove(input_file_path)
    return new_srt_path

def add_subtitles_to_video(new_srt_filepath, video_path, styles=None):
    # Дефолтные значения стиля
    default_style = {
        'font': "Arial",
        'fontsize': 24,
        'color': 'white',
        'bg_color': 'black',
        'position': ('center', 'bottom')
    }
    
    # Если стиль не передан, используем дефолтный
    if styles is None:
        styles = default_style
    else:
        # Заполняем отсутствующие параметры дефолтными значениями
        styles = {**default_style, **styles}
    
    # Загрузить видео
    video = VideoFileClip(video_path)
    width, height = get_video_resolution(video_path)
    video = video.resize(newsize=(width, height))
    subs = pysrt.open(new_srt_filepath)
    
    # Преобразовать субтитры в формат, который принимает moviepy
    def make_text_clip(sub):
        # Конвертируем время в секунды
        start_time = sub.start.seconds + sub.start.milliseconds / 1000.0
        end_time = sub.end.seconds + sub.end.milliseconds / 1000.0
        
        return TextClip(sub.text,
                        fontsize=styles['fontsize'],
                        color=styles['color'],
                        bg_color=styles['bg_color'],
                        font=styles['font'],
                        align="center") \
            .set_position(styles['position']) \
            .set_duration(end_time - start_time) \
            .set_start(start_time)
    
    subtitle_clips = [make_text_clip(sub) for sub in subs]
    video_with_subs = CompositeVideoClip([video] + subtitle_clips)
    
    # Генерация пути для выходного файла с суффиксом "_changed"
    output_filename = os.path.splitext(os.path.basename(video_path))[0] + "_changed" + os.path.splitext(video_path)[1]
    unique_id = generate_random_hash()
    output_folder = f"results/{unique_id}"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)

    # Экспортировать новое видео с сохранением оригинального соотношения сторон и качества
    video_with_subs.write_videofile(output_path, codec="libx264", fps=video.fps, preset="slow", threads=4, bitrate="5000k")
    
    os.remove(new_srt_filepath)
    return output_path

def get_subs(video_path, styles):
    audio_path = extract_audio_from_video(video_path)
    srt_filepath = convert_audio_to_srt(audio_path)
    new_srt_filepath = str_rewriter_by_words(srt_filepath, words= 5)
    output_path = add_subtitles_to_video(new_srt_filepath, video_path, styles=styles)
    return output_path


if __name__ == '__main__':
    video_path = '/Users/maratorozaliev/Desktop/brainrot/IMG_0061.MOV'
    styles = {
        'font': "Arial",                        # тип <str>, Шрифт текста - "Arial", "Courier-Bold", "Verdana"
        'fontsize': 50,                         # тип <int>, Размер шрифта в пикселях - 24, 30, 40
        'color': 'black',                       # тип <str>, Цвет текста - "white", "yellow", "red", "blue", "green" или html код - "#ff0000"
        'bg_color': 'white',                    # тип <str>, Цвет фона - также как и color
        'position': ('center', 'bottom')        # тип <tuple>, Позиция текста на экране ('center', 'bottom'), ('left', 'top'), ('right', 'center')
    }
    get_subs(video_path, styles)
    print(video_path)

