import requests
import os

from dotenv import load_dotenv

load_dotenv()
elevenlabs_api_key = os.getenv('MY_ELEVENLABS_API_KEY')

def convert_to_speech_eleven(text, filename):
    print('synthesizing speech')
    data = {
      "text": text,
      "model_id": "eleven_multilingual_v1",
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


# Read contents of file hindi.txt into a string
with open('other/hindi.txt', 'r') as file:
    content = file.read()

convert_to_speech_eleven(content, 'other/speech')