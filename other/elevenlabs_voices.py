import requests
import json
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

url = "https://api.elevenlabs.io/v1/voices"

headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": elevenlabs_api_key
}

response = requests.get(url, headers=headers)
response = json.loads(response.text)

for voice in response['voices']:
    print(voice['name'])
    print(voice['voice_id'])

voice_id = response['voices'][-3]['voice_id']

def convert_to_speech_eleven(text, voice_id):
    print('synthesizing speech')
    data = {
      "text": text,
      "model_id": "eleven_multilingual_v1",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }


    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id


    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": elevenlabs_api_key
    }

    response = requests.post(url, json=data, headers=headers)

    print(response)
    
    return response.iter_content(chunk_size=CHUNK_SIZE)

story = """
Once upon a time, in a small, sleepy town nestled in the heart of the countryside, there lived a curious and adventurous young boy named Mat. Mat had always been different from the other children in town. While they were content playing in their backyards or cycling around the neighborhood, Mat's heart yearned for something more. He often spent his afternoons gazing out at the horizon, dreaming of far-off lands and thrilling adventures.

Mat's parents, John and Susan, encouraged their son's curiosity and adventurous spirit. They believed that every child should have the opportunity to explore the world around them. John, an avid traveler himself, would often regale Mat with tales of his own adventures in distant lands. Susan, a naturalist, would take Mat on long hikes through the lush forests that surrounded their town, teaching him about the wonders of the natural world.

One bright summer morning, Mat woke up with an overwhelming feeling of restlessness. He couldn't shake the desire to embark on an adventure of his own. He rushed downstairs, where his parents were sipping their morning coffee.

"Mom, Dad, I've decided I want to go on a grand adventure," Mat declared with a determined look in his eyes.

John and Susan exchanged knowing glances. They had expected this day to come sooner or later.

"Mat, that's a wonderful idea," Susan said, smiling warmly. "But remember, with adventure comes responsibility and preparation. You must be ready for whatever challenges may come your way."

John nodded in agreement. "We'll help you plan and prepare for your journey, son. It's important to be well-equipped and informed."

Over the following weeks, Mat immersed himself in books about survival, navigation, and the history of explorers who had charted unknown territories. He also spent countless hours with his father, learning valuable skills like setting up a campfire, reading maps, and using a compass. Mat's mother, Susan, taught him about the plants and animals he might encounter in the wild, emphasizing the importance of respecting and preserving the environment.

Finally, the day of Mat's departure arrived. With a backpack filled with supplies, a map in hand, and the unwavering support of his parents, Mat set off on his grand adventure. His destination was a remote forest on the outskirts of town, a place few had ever ventured into.
"""

voice_id = "B6iuPRFYgnWhC9SAo8BS" # Tamika
bytes = convert_to_speech_eleven(story, voice_id)

with open('output/v2/speech.mp3', 'wb') as f:
    for chunk in bytes:
        f.write(chunk)
