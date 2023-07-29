import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

def convert_to_speech(text, filename):
    print('synthesizing speech')
    data = {
      "text": text,
      "model_id": "eleven_monolingual_v1",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }

    josh_voice_id = "TxGEqnHWrfWFTfGW9XjX"

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + josh_voice_id


    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": elevenlabs_api_key
    }

    response = requests.post(url, json=data, headers=headers)
        
    with open(filename + '.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

if __name__ == '__main__':
  convert_to_speech("Cats! I'm a kitty cat. And I dance dance dance, and I dance, dance, dance.", "output")