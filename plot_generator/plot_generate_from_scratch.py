import openai
from dotenv import load_dotenv
import os
from openai import OpenAI
import ast
import re

load_dotenv()

def generate_base_plot(prompt):
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system", "content": "Return the plot in string format and nothing more"
            },
            {
            "role": "user", "content": prompt
            }
            ],
        temperature=0.9
    )
    answer = response.choices[0].message.content
    return answer

def find_characters(story):
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", "content": "Find every character(s) in story and return all of them separating by comma and nothing more"
            },
            {
            "role": "user", "content": story
            }
            ],
        temperature=0.4
    )
    answer = response.choices[0].message.content
    return answer

def characters_look(characters):
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", "content": """
                You will be given a list of characters. 
                You need to imagine the appearance of each character by 4 attributes (age, nation, hair color, sex) and return answer in dictionary format.
                Your answer should look like this:
                {
                'character_name': 'young russian blonde girl',
                'character_name': 'old arabian brunette guy',
                'character_name': 'robotic brunette figure',
                ...
                }
                """
            },
            {
            "role": "user", "content": characters
            }
            ],
        temperature = 0.2
    )
    answer = response.choices[0].message.content
    return answer

def split_idea(prompt):
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", "content": """
                Split the plot into several logical scenes.
                Follow the format:
                [
                    {
                    'narrator' : "text for narrator",
                    'dalle' : "scene description including characters from narrative", 
                    },
                    {
                    'narrator' : "text for narrator",
                    'dalle' : "scene generation including characters from narrative",
                    },
                    ...
                ]
                """
            },
            {
            "role": "user", "content": prompt
            }
            ],
        temperature=0.8
    )
    answer = response.choices[0].message.content
    return answer

def change_prompt_based_on_character(prompt, characters):
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", "content": """
                If there are ANY characters in the prompt, add the description of a character nearby in brackets.
                Return the content of a changed prompt.
                """
            },
            {
            "role": "user", "content": f"""
            Prompt: {prompt}
            Character list: {characters}
            """
            }
            ],
        temperature=0.1
    )
    answer = response.choices[0].message.content
    return answer

def validate_story_elements(idea):
    required_keys = {'dalle', 'narrator'}

    for i, element in enumerate(idea):
        if not required_keys.issubset(element.keys()):
            return False
    return True

def replace_non_standard_chars(input_string):
    return re.sub(r'[—–]', '-', input_string)

def build_whole_story(prompt):
    plot = generate_base_plot(prompt)
    idea = split_idea(plot)
    idea = replace_non_standard_chars(idea)
    idea = ast.literal_eval(idea)
    if validate_story_elements(idea):
        story = []
        voice_lines = []
        for dalle_and_narrator in idea:
            story.append(dalle_and_narrator['dalle'])
            voice_lines.append(dalle_and_narrator['narrator'])

        characters = find_characters(''.join(story))
        characters = '[' + characters + ']'
        characters = characters_look(characters)
        characters = replace_non_standard_chars(characters)
        characters = ast.literal_eval(characters)
        finalised = []
        for dalle_prompt in story:
            changed_prompt = change_prompt_based_on_character(dalle_prompt, characters)
            changed_prompt = changed_prompt.replace('Prompt:', '')
            finalised.append(changed_prompt)
        
    return finalised, voice_lines

if __name__ == '__main__':
    # Пример использования
    prompt = "Write a plot for a one-minure story about travelling in time."
    finalised, voice_lines = build_whole_story(prompt=prompt)
    print(finalised, voice_lines)
    for i, j in zip(finalised, voice_lines):
        print()
        print('story:', i)
        print('narrator:', j)
    print("GOOD job bro!") 