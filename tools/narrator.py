from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from tools.generate_id import generate_random_hash

def voicing(voice_line, narrator_voice, filename = 'output.mp3'):
    if narrator_voice in ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']:
        model_voice = narrator_voice
    else:
        model_voice = 'onyx'
        
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        )

    response = client.audio.speech.create(
        model="tts-1",
        voice=model_voice,
        input=voice_line,
    )

    response.stream_to_file(filename)

def voice_the_narrative(NARRATOR, narrator_voice):
    unique_id = generate_random_hash()
    audio_folder = f"media/onyx_cooked/{unique_id}"
    os.makedirs(audio_folder, exist_ok=True)

    for index, scene_narrative in enumerate(NARRATOR, start=1): 
        filename = f"{audio_folder}/narrative_{index}.mp3"
        voicing(scene_narrative, narrator_voice = narrator_voice, filename = filename)

    return audio_folder

if __name__ == '__main__':
        
    # NARRATOR = ['In a cluttered attic filled with forgotten relics, 17-year-old Mia discovers an old pocket watch belonging to her late grandfather. The air is thick with dust, and beams of sunlight slice through the dimness.', 'As she winds the pocket watch, a strange energy envelops her. Suddenly, she is transported to the year 1965, landing in the midst of a bustling city street filled with classic cars and people in vibrant vintage fashion.', 'Confused but intrigued, Mia wanders through the vibrant world. She encounters a young man named Jack, who seems to recognize her, claiming they are destined to meet.', 'Together, they explore the city, sharing dreams and laughter, feeling an undeniable connection. But as the sun begins to set, Mia senses the pull of time calling her back.', 'Desperate to stay, Mia learns that the watch can only function for one hour. Time is running out, and she must make a choice.', 'With just minutes to spare, Mia faces her decision: return to her own time or risk altering history by staying with Jack. Ultimately, she chooses to return.', 'As she winds the watch one last time, Mia leaves Jack with a coded message that he will decipher years later, a hint of their time-traveling love.', 'Mia returns home, clutching the watch tightly, knowing that their bond transcends time itself.']
    # audio_folder = voice_the_narrative(NARRATOR)
    pass