import openai
import boto3
import os
import uuid
import io
import time
import argparse
import json
import requests

import random
import re
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import numpy as np
from pydub import AudioSegment

from dotenv import load_dotenv

from create_episode import generate_episode
# from eleven import elevenlabs
load_dotenv()


def call_anthropic_api(prompt):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    anthropic = Anthropic(
        api_key=api_key,
    )
    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=5000,
    prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
    )
    return completion.completion

def call_openai_api(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Define the parameters for the completion
    params = {
        'model': 'text-davinci-003',  # The model you want to use
        'prompt': prompt,
        'max_tokens': 3000,
        'temperature': 0.7,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }

    # Call the OpenAI API
    response = openai.Completion.create(**params)

    # Retrieve the generated text from the API response
    generated_text = response.choices[0].text.strip()

    return generated_text

def sythesize_speech_aws(text):
        # Create a client using your AWS access keys stored as environment variables
    polly_client = boto3.Session(
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')).client('polly')

    response = polly_client.synthesize_speech(
        VoiceId='Matthew',      
        Engine='neural',
        OutputFormat='mp3',
        Text = text
    )

    # The response body contains the audio stream.
    # Writing the stream in a mp3 file
    filename = 'output/speech.mp3'
    with open(filename, 'wb') as file:
        file.write(response['AudioStream'].read())

    print('output saved in output/speech.mp3')

elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")

def convert_to_speech_eleven(text, filename):
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


def synthesize_speech_eleven(text):
    # Create a client using your AWS access keys stored as environment variables

    convert_to_speech_eleven(text, 'output/speech')
    print('output saved in output/speech.mp3')

def get_serpapi_search_results(query):
    base_url = "https://serpapi.com/search"
    params = {
        'q': query,
        'api_key': os.getenv("SERPAPI_API_KEY"),
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        print(json.loads(response.text))
        # 1/0
        return json.loads(response.text)
    else:
        return None


from joblib import Memory
import time

# Choose a location for the cache
cachedir = './cache_dir'
memory = Memory(cachedir, verbose=0)
@memory.cache
def enrich_topic(topic):
    relevance_prompt = f"""
    Help me identify the most important pieces of information we need to search up on Google 
    in order to gather recent relevant knowledge to generate a podcast. 
    Output the most relevant part of the topic the user entered which we should search up on Google.
    Topic: {topic}
    The output format should look like this:
    {{
        "google_search_topic": "IDENTIFIED_TOPIC"
    }}
"""
    # Get the most relevant search topic
    # Try 3 times before failing
    added_prompt = ""
    try:
        relevant_search_topics = call_anthropic_api(relevance_prompt)
        
        relevant_search_topics = json.loads(relevant_search_topics)
        relevant_search_topic = relevant_search_topics['google_search_topic']

        relevant_search_topic = topic

        print('relevant_search_topic')
        print(relevant_search_topic)

        # Get the top 3 results from Google
        google_search_results = get_serpapi_search_results(relevant_search_topic)
        from pprint import pprint
        print('google_search_results')
        pprint(google_search_results)

        added_prompt = """Here is some information we pulled from Google on the user's query.
        Use this information if you feel it is relevant.\n\nSTART_SEARCH_RESULTS"""
        added_prompt += str(google_search_results) + "\n\n"

        added_prompt += "END_SEARCH_RESULTS\n\n"

        # if google_search_results:
        #     # print('cats')
        #     # pprint(google_search_results['organic_results'][:1])
        #     for result in google_search_results['organic_results'][:3]:
        #         if 'snippet' in result:
        #             added_prompt += result['snippet'] + "\n\n"
        #     #     print('chris1')
        #     #     print(result)
        #         if 'rich_snippet' in result:
        #             added_prompt += str(result['rich_snippet']) + "\n"
                
        #         if 'rich_snippet_list' in result:
        #             added_prompt += str(result['rich_snippet_list']) + "\n"

        #             # for rich_snippet in result['rich_snippet_list']:
        #             #     if 'snippet' in rich_snippet:
        #             #         added_prompt += rich_snippet['snippet'] + "\n\n"
        # else:
        #     added_prompt += str(google_search_results) + "\n\n"
    except Exception as e:
        print(f"Caught an exception: {e}")


    print('added_prompt')
    print(added_prompt)

    return topic + "\n\n" + added_prompt

def create_podcast_prompt(topic, duration, tone):
    # Create the podcast prompt
#     meta_prompt = f"""
# Please help me to make a prompt to GPT-3 to generate a podcast about {topic}.
# The prompt should instruct GPT that the podcast should be {duration} minutes long.
# The prompt should instruct GPT to only reply with the text of the podcast it generates.
# The prompt should instruct GPT that the podcast would be with 1 person only, and not try to switch between multiple people.
# The prompt should instruct GPT to make the podcast seem like a fluid conversation, without breaks in the conversation.
# The prompt should instruct GPT that the text of the response should be the transcript of the podcast.
# There should be no seperator between the segments, so that the podcast is one continuous audio file.
# Please only output a prompt that I can use to send to GPT.
# """

    enriched_topic_info = enrich_topic(topic)

    # For each result, get the text from the page

    content_type = "story" if tone == "Story" else "podcast"

    prompt = f"""
Create the audio transcript of a {content_type} about {topic}.
The {content_type} should be {duration} minutes long.
The speaker of the {content_type} should talk in a very {tone} tone.
I would like to reiterate, emphasize the {tone} tone. Be very {tone} please. It is an important business requirenment that you are {tone}.
The {content_type} should be with 1 person only, and not try to switch between multiple people.
The {content_type} should seem like a fluid conversation, without breaks in the conversation.
The text of the response should be the transcript of the {content_type}.
There should be no seperator between the segments, so that the {content_type} is one continuous audio file.
{enriched_topic_info}
"""
    return prompt

def create_podcast(topic, duration, tone):
    prompt = create_podcast_prompt(topic, duration, tone)

    print(prompt)

    story = call_openai_api(prompt)

    print("Here is the story:")
    print(story)

    sythesize_speech_aws(story)
    # synthesize_speech_eleven(story)

    # Generate a UUID
    folder_name = str(uuid.uuid4())

    # Name of the parent folder
    parent_folder = './outputs'

    # Ensure the parent folder exists
    os.makedirs(parent_folder, exist_ok=True)

    # Create the full path for the new folder
    full_path = os.path.join(parent_folder, folder_name)
    full_path = './outputs/' + folder_name

    # Create a new folder with the UUID as the name
    os.makedirs(full_path, exist_ok=True)

    # Your string to be saved
    prompt_and_podcast = prompt + "\n\n" + story

    # Write the string to a new file in the new folder
    with open(full_path + '/prompt_and_podcast.txt', 'w') as f:
        f.write(prompt_and_podcast)

    print('wrote file')

    return story

def create_podcast_expensive(topic, duration, tone):
    prompt = create_podcast_prompt(topic, duration, tone)
    print(prompt)
    story = call_openai_api(prompt)

    print("Here is the story:")
    print(story)

    synthesize_speech_eleven(story)
    return story

def create_emotional_podcast(topic, d, o):
    enriched_topic_info = enrich_topic(topic)
    share_url = generate_episode(enriched_topic_info, topic, d)
    return share_url

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Podcast Generator')
    parser.add_argument('-t', '--topic', required=True,  help='Topic of the podcast')
    parser.add_argument('-d', '--duration', required=True, help='Duration of the podcast in minutes')
    parser.add_argument('-o', '--tone', required=True, help='Tone the speaker should speak in')
    # Example args:
    # python src/gen_podcast.py -t "Adam D'Angelo" -d 10 -o "Professional"
    args = parser.parse_args()
    topic = args.topic
    duration = args.duration
    tone = args.tone

    # topic = "Finding a girlfriend in the bay area as an Indian Software Engineer"
    # duration = 10
    
    # create_podcast(topic, duration, tone)
    create_emotional_podcast(topic, duration, tone)
