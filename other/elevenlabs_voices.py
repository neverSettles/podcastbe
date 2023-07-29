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

pprint(response)