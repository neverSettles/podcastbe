
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
from time import sleep


import requests
import json

# url = "https://api.v5.unrealspeech.com/synthesisTasks"

# payload = json.dumps({
#     "Text": "A startup is a company designed to grow fast. Being newly founded does not in itself make a company a startup. Nor is it necessary for a startup to work on technology, or take venture funding, or have some sort of \"exit.\" The only essential thing is growth. Everything else we associate with startups follows from growth.",
#     "VoiceId": "male-0",
#     "Bitrate": "320k",
#     "AudioFormat": "mp3",
#     "OutputFormat": "uri"
# })
# headers = {
#     'Authorization': 'Bearer jeremy_temp_api_key',
#     'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# # print(response.text)
# print(response.json())

# OutputUri = response.json()['SynthesisTask']['OutputUri']

# sleep(5)

# import requests
# # url = "https://unreal-tts-live-demo.s3-us-west-1.amazonaws.com/5c531308.mp3"
# # url = "https://unreal-tts-live-demo.s3-us-west-1.amazonaws.com/84cf3838.mp3"
# response = requests.get(OutputUri)

# # To save the content to a file
# with open("output/unreal/sample.mp3", "wb") as file:
#     file.write(response.content)

url = "https://api.v5.unrealspeech.com/synthesisTasks"

voices = [
    # male-0, male-1, male-2, male-3, male-4, dev-0, dev-1, dev-2, dev-3, v6-male-0, v6-male-1, v6-female-0, v6-female-1
    # 'male-0',
    # 'male-1',
    # # fill in the rest
    # 'male-2',
    # 'male-3',
    # 'dev-0',
    # 'dev-1',
    # 'dev-2', # obama
    'dev-3', # peterson
    'Amy',
    'Dan',
]

potential_voices = [
    'v6-male-0',
    'v6-male-1',
    'v6-female-0',
    'v6-female-1'
]

text_to_speak = """
Golden ears stand tall and proud,
Whispers rustle, soft yet wowed.
Nature's bounty, rows align,
Corn's sweet gift, sun's design.
"""

text_to_speak = """
Today, I'd like to discuss a topic that's close to my heart: the superiority of the Cassandra database. Let me outline the reasons why I believe Cassandra stands out in the world of databases.

First and foremost, scalability. Cassandra is renowned for its horizontal scalability. As your data grows, you can effortlessly add more nodes to the cluster without any downtime, ensuring consistent performance.

"""

def convert_to_speech_bytes_stream(text, voice):
    response = requests.post(
    'https://api.v6.unrealspeech.com/stream',
    headers = {
        'Authorization' : 'Bearer ' + os.getenv('UNREAL_API_KEY')
    },
    json = {
        'Text': text,
        'VoiceId': voice,
        'Bitrate': '128k',
    }
    )

    print(response)

    return response.content

def convert_to_speech_bytes_synthesisTasks(text, voice):
    response = requests.post(
    'https://api.v6.unrealspeech.com/synthesisTasks',
    headers = {
        'Authorization' : 'Bearer ' + os.getenv('UNREAL_API_KEY')
    }, json = {
        'Text': text,
        'VoiceId': voice,
        'Bitrate': '128k',
    })

    print(response)

    fetch_url = response.json()['SynthesisTask']['OutputUri']

    print('fetch_url')
    print(fetch_url)

    MAX_RETRIES = 40

    for i in range(MAX_RETRIES):
        sleep(0.5)
        response = requests.get(fetch_url)
        if response.status_code == 200:
            print('success after ' + str(i) + ' retries')
            return response.content
        else:
            print(response.status_code)
    
    return None


for voice in voices:
    # There are 2 APIs: stream (500 characters) and speechTasks (500,000 chars)
    response = convert_to_speech_bytes_synthesisTasks(text_to_speak, voice)

    # print(response.text)

    with open("output/unreal/" + voice + ".mp3", 'wb') as f:
        f.write(response)

