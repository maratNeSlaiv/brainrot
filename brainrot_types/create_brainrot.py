from tools.plot_generate_from_scratch import build_whole_story
from tools.generate_id import generate_random_hash
import os
from tools.narrator import onyx_for_voicing
from tools.narrator import voice_the_narrative
from tools.dalle_scenes import create_the_scenes
from tools.combine_audio_with_generated_images import create_slideshow_with_audio
import sys

def make_ai_generated_story(prompt, narrator_voice = 'onyx'):
    FINALISED, NARRATOR = build_whole_story(prompt=prompt)

    for i, j in zip(FINALISED, NARRATOR):
        print()
        print('story:', i)
        print('narrator:', j)
    
    go_further = input("Are we good with the narrative and prompts for dalle? type 'YES' in that case:")
    if go_further == "YES":
        audio_folder = voice_the_narrative(NARRATOR, narrator_voice = narrator_voice)
        print('Audio folder:', audio_folder)
        image_folder = create_the_scenes(FINALISED)
        print('Image folder:', image_folder)
        
        unique_id = generate_random_hash()
        folder = f"results/{unique_id}"
        os.makedirs(folder, exist_ok=True)
        output_filename = f"{folder}/story.mp4"
        create_slideshow_with_audio(image_folder, audio_folder, output_filename=output_filename)
        print('Generated video located at:', output_filename)
    else:
        sys.exit('Run again to generate different story')

if __name__ == '__main__':
    prompt = "Write a plot for a one-minure story about travelling in time."
    make_ai_generated_story(prompt, narrator_voice = 'onyx')
    "For narrator voice you can choose from: 'alloy', 'echo', 'fable', 'onyx', 'nova', and 'shimmer'"
    # Check how they sound at https://platform.openai.com/docs/guides/text-to-speech