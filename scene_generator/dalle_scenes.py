import openai
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os
import requests
from tools.generate_id import generate_random_hash

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )

def generate_image(prompt):
    response = client.images.generate(
        prompt=prompt,
        # quality='hd',
        model="dall-e-3",
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    return image_url

# Example prompt
def save_image(image_url, filename="generated_image.png"):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
    else:
        print("Failed to retrieve image")

def create_the_scenes(FINALISED):
    unique_id = generate_random_hash()
    dalle_folder = f"dall-e/{unique_id}"
    os.makedirs(dalle_folder, exist_ok=True)

    for index, scene_prompt in enumerate(FINALISED, start=1):
        image_url = generate_image(scene_prompt)
        # print(image_url)
        filename = f"{dalle_folder}/generated_img{index}.png"
        save_image(image_url, filename=filename)

    return dalle_folder

# Usage
if __name__ == '__main__':
    FINALISED = [
        ' A teenage girl, Mia (teenage, brown hair, Caucasian), stands in a cluttered attic surrounded by boxes and old furniture, holding an ornate vintage pocket watch. Sunlight filters through a small window, highlighting cobwebs and dust motes.', 
        ' Mia (teenage, brown hair, Caucasian), now in 1965 attire, stands in a lively city street surrounded by colorful vintage cars and pedestrians dressed in 60s fashion. Bright shop signs and neon lights illuminate the scene.', 
        ' Mia (a teenage girl with brown hair and a Caucasian complexion) meets Jack (a young man with dark hair and a Caucasian complexion, dressed in a retro outfit), with a charming smile. They stand on the sidewalk, surrounded by bustling city life, exchanging curious looks and laughter.', 
        ' Mia (a teenage girl with brown hair, Caucasian) and Jack (a young man with dark hair, Caucasian) are laughing together in front of a diner as the sun sets, casting a warm glow. They sit on a bench, enjoying milkshakes, with the skyline silhouetted against the colorful sky.', 
        ' Mia (teenage, brown hair, Caucasian) looks intently at the pocket watch, a worried expression on her face, while Jack (young man, dark hair, Caucasian) watches her with concern. The sunset casts long shadows, indicating the passage of time.', 
        ' Mia (teenage, brown hair, Caucasian) stands with Jack (young man, dark hair, Caucasian), tears in her eyes as she prepares to leave. The street is illuminated by the last rays of sunlight, and Jack reaches out to her, looking heartbroken.', 
        ' Mia (teenage girl, brown hair,Caucasian) is about to vanish, holding the watch in one hand and a small piece of paper with a coded message in the other. Jack (young man, dark hair, Caucasian), whose expression filled with determination looks at her, longing to understand.', 
        'Back in her attic, Mia (a teenage girl with brown hair and a wistful expression) stands in the warm glow of the sunset filtering through the window, holding the pocket watch close to her heart, a mix of nostalgia and hope on her face.'
                 ]
    
    dalle_folder = create_the_scenes(FINALISED)