import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from pydub.utils import mediainfo

# Function to get the duration of an audio file
def get_audio_duration(audio_path):
    audio_info = mediainfo(audio_path)
    return float(audio_info['duration'])

# Function to create a video from PNG and corresponding audio files with smooth transitions
def create_slideshow_with_audio(image_folder, audio_folder, output_filename="output_video.mp4", transition_duration=1):
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.mp3') or f.endswith('.wav')])
    
    clips = []
    
    for image_file, audio_file in zip(image_files, audio_files):
        # Get the full path to the image and audio files
        image_path = os.path.join(image_folder, image_file)
        audio_path = os.path.join(audio_folder, audio_file)
        
        # Get the duration of the audio file
        audio_duration = get_audio_duration(audio_path)
        
        # Create an ImageClip for the current image
        img_clip = ImageClip(image_path, duration=audio_duration)
        img_clip = img_clip.set_audio(AudioFileClip(audio_path))  # Set corresponding audio
        
        clips.append(img_clip)
    
    # Apply crossfade between all clips
    final_clips = []
    for i in range(len(clips) - 1):
        # Apply the crossfade effect
        crossfaded_clip = clips[i].crossfadeout(transition_duration).crossfadein(transition_duration)
        final_clips.append(crossfaded_clip)
    
    # Add the last clip without transition
    final_clips.append(clips[-1])

    # Concatenate all clips with transitions to make the final video
    final_clip = concatenate_videoclips(final_clips, method="compose")
    
    # Write the final video to a file
    final_clip.write_videofile(output_filename, codec='libx264', fps=24)

if __name__ == '__main__':
    image_folder = '/Users/maratorozaliev/Desktop/brainrot/dall-e/2275ead719b42ead/'
    audio_folder = '/Users/maratorozaliev/Desktop/brainrot/onyx_cooked/302de7f17a37345b/'
    create_slideshow_with_audio(image_folder, audio_folder)
