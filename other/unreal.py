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
    'dev-2', # obama
    'dev-3', # peterson
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

Now, let's talk about availability. With its distributed architecture, Cassandra ensures there are no single points of failure. Even if several nodes were to fail, the database remains operational. This level of reliability is paramount for businesses that can't afford any downtime.
"""

# text_to_speak = """
# Mat lived in a quiet village, where nothing ever changed. One day, while exploring the forest, he stumbled upon a hidden cave. Inside, he found a shimmering, ancient amulet. As he touched it, memories of past heroes flooded his mind. The amulet granted him the wisdom of ages. With newfound knowledge, Mat transformed his village, introducing innovations and teaching forgotten arts. The once-sleepy village thrived, becoming a beacon of hope. Mat, once an ordinary boy, was now the village's cherished sage, all thanks to a chance discovery in the woods.
# """

for voice in voices:
    payload = json.dumps({
    "Text": text_to_speak,
    "VoiceId": voice,
    "Bitrate": "320k",
    "AudioFormat": "mp3",
    "OutputFormat": "uri"
    })

    key = os.getenv("UNREAL_API_KEY")

    headers = {
    'Authorization': 'Bearer ' + str(key),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print('response')
    print(response.text)

    fetch_url = response.json()['SynthesisTask']['OutputUri']

    print('fetch_url')
    print(fetch_url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    sleep(5)
    with requests.Session() as session:
        audio = session.get(fetch_url, headers=headers)
    # audio = requests.get(fetch_url)

    # save audio locally
    print (audio)
    with open("output/unreal/" + voice + ".mp3", 'wb') as f:
        f.write(audio.content)