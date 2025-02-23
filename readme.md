Brainrot is a mini-project that uses openai GenAI tools to create random videos from a prompt.
Pipeline is as follows:
1) create scenario/narrative
2) create images to match the scenario
3) Voice the narrative
4) Combine images with audio as slideshow
5) Optional subs (You can add subtitles of any style at any place, using tools/get_subs.py file)

I'm using python 3.11.10, since whisper (model to convert audio to text (for subs purpose)) needs a 3.9 - 3.11 versions of python.

Get the project working:
1) create virtual environment
2) install dependencies
3) create '.env' file and add OPENAI_API_KEY = 'your_api_key'
4) run brainrot_types/create_brainrot.py:
    * run 'export PYTHONPATH=/path/to/the/project/root' in case python can't see modules
5) It takes approximately 15-20 seconds to generate a scenario. Type 'YES' if everything in scenario looks fine. It will take another 1 or 2 minutes to generate pictures, voice the narrative and create a slideshow video in results/some_hash.
    * If you want to apply subs: it will take more time on the first get_subs.py run, because of a load of the whisper model, which weighs around 3 gb.

Each generated video costs around ~30 cents (3.5 cents for every generated image, 1-2 cents for narrator voicing, and < 1 cent for scenario generation). I believe after some time, generation of images will be much cheaper. 

Place that may be optimized is sending calls to DALL-E from tools/dalle_scenes.py. Usage of asyncronous programming will speed up the process several times.
