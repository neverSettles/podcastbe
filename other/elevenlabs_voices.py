import requests
import json
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

url = "https://api.elevenlabs.io/v1/voices"

headers = {
  "Accept": "application/json",
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

story = "Mat found a glowing stone. At night, it whispered tales of ancient heroes. He became one."
bytes = convert_to_speech_eleven(story, voice_id)

with open('output/v2/speech.mp3', 'wb') as f:
    for chunk in bytes:
        f.write(chunk)
