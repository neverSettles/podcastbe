# User prompt in.
# Characters Out. Names + Descriptions.
# Characters + Users -> Outline.
# Characters + Users + Outline -> Sub-Outlines.
# Recursively Process Outline, section by section, passing in the existing text.

import random
import re
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
# from elevenlabslib import *
import numpy as np
from pydub import AudioSegment
from dotenv import load_dotenv
import requests
import os
import boto3
from time import sleep

load_dotenv()


TOTAL_PARTS = 2
PARTS_PER_SECTION = 2
MIN_HOSTS = 2
MAX_HOSTS = 2

api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic = Anthropic(
    api_key=api_key,
)

# eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
# user = ElevenLabsUser(eleven_labs_api_key)


def generate(prompt):
    completion = anthropic.completions.create(
        model="claude-instant-v1",
        max_tokens_to_sample=5000,
        prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
    )
    return completion.completion


def parse_podcast_text_sequence(text):
    # split the text into separate dialogue entries
    dialogues = re.split(r"<Speaker \d+>", text)
    # remove empty strings
    dialogues = list(filter(None, dialogues))
    # initialize the list
    result = []
    # iterate over the dialogues
    for dialogue in dialogues:
        # check if the dialogue contains a colon
        if ":" in dialogue:
            # split the dialogue into the speaker and the message
            speaker, message = dialogue.split(":", 1)
        else:
            # if the dialogue doesn't contain a colon, skip it
            continue

        # remove leading and trailing whitespace
        speaker = speaker.strip()
        message = message.strip()
        # remove the closing </Speaker> tag from the message
        message = re.sub(r"</Speaker \d+>", "", message)
        # append the dialogue to the result list
        result.append({speaker: message})
    return result


def dict_to_string(dialogue_dict):
    string = ""
    for key, value in dialogue_dict.items():
        string += f"{key}: {value} "
    return string.strip()


def get_gender(host_name):
    result = generate(
        f"""Is the name {host_name} male or female? Answer with a single word, either "Male" or "Female"."""
    ).strip()
    return result


def voice_choice(host_list):
    male_voices = [
        {
            "aws": "Matthew",
            "unreal": "Dan",
            "eleven": "B6iuPRFYgnWhC9SAo8BS", # Oswald - intelligent professor
            # "eleven": "ODq5zmih8GrVes37Dizd", # Arnold
        },
        # "Stephen",
    ]

    female_voices = [
        {
            "aws": "Joanna", 
            "unreal": "Amy",
            # "eleven": "a8uAokkpYQj8j7Bs7SaP", # Tamika
            "eleven": "XB0fDUnXU5powFXDhCwa", # Charlotte
            
        },
        # "Salli",
    ]

    host_voice = {}
    for host in host_list:
        gender = get_gender(host)
        if gender == "Male":
            voice_idx = random.randint(0, len(male_voices) - 1)
            host_voice[host] = male_voices[voice_idx]
            male_voices.pop(voice_idx)
        else:
            voice_idx = random.randint(0, len(female_voices) - 1)
            host_voice[host] = female_voices[voice_idx]
            female_voices.pop(voice_idx)
    return host_voice

def synthesize_speech(voice, text):
        # Use Amazon Polly to convert text to speech
        polly_client = boto3.Session(
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                        region_name=os.getenv('AWS_REGION', 'us-east-1')).client('polly')

        response = polly_client.synthesize_speech(
            VoiceId=voice['aws'],
            OutputFormat='mp3',
            Engine='neural',
            Text=text
        )

        # Assuming you've already made the request and have the response
        audio_stream = response['AudioStream']
        return audio_stream.read()

def convert_to_speech_bytes_synthesisTasks(voice, text):
    response = requests.post(
    'https://api.v6.unrealspeech.com/synthesisTasks',
    headers = {
        'Authorization' : 'Bearer ' + os.getenv('UNREAL_API_KEY')
    }, json = {
        'Text': text,
        'VoiceId': voice['unreal'],
        'Bitrate': '128k',
    })

    if response.status_code != 200:
        print(response.text)
        print('erroring out, falling back to aws')
        return synthesize_speech(voice, text)

    fetch_url = response.json()['SynthesisTask']['OutputUri']

    print('fetch_url')
    print(fetch_url)

    MAX_RETRIES = 80

    for i in range(MAX_RETRIES):
        sleep(1)
        response = requests.get(fetch_url)
        if response.status_code == 200:
            print('success after ' + str(i) + ' retries')
            return response.content
        elif i%10 == 9:
            print(response.status_code)
    
    print('erroring out, falling back to aws')
    return synthesize_speech(voice, text)

def convert_to_speech_eleven(voice, text):
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
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice['eleven']
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")


    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": elevenlabs_api_key
    }

    print('Sending eleven labs request...')
    print(url)
    print(data)
    print(headers)

    response = requests.post(url, json=data, headers=headers)

    print(response)
    if response.status_code == 400:
        print("HTTP 400 Bad Request")
        print(response.text)  # Print the raw response
    if response.status_code == 401:
        print("HTTP 400 Bad Request")
        print(response.text)  # Print the raw response
    
    return b''.join(response.iter_content(chunk_size=CHUNK_SIZE))

def bytes_to_audio_segment(
        audio_bytes, sample_rate=44100, sample_width=2, channels=1
    ):
        audio_arr = generate_audio_robust(audio_bytes)
        return AudioSegment(
            audio_arr.tobytes(),
            frame_rate=sample_rate,
            sample_width=sample_width,
            channels=channels,
        )

def generate_audio_robust(audio_bytes, max_retries=10, retry_delay=5):
        for attempt in range(max_retries):
            try:
                audio_arr = np.frombuffer(audio_bytes, dtype=np.int16)
                print("Success.")
                return audio_arr
            except ValueError:
                print("Hit Exception")
                if len(audio_bytes) % 2 != 0:
                    audio_bytes = audio_bytes[:-1]  # remove the last byte
                    audio_arr = np.frombuffer(audio_bytes, dtype=np.int16)
                    print("Exception Overcome. Success.")
                    return audio_arr
                
def dict_to_audio(dialogue_dict,host_voice, filename="audio"):
        string = ""
        for key, value in dialogue_dict.items():
            string += f"{key}: {value} "
            # replace elevenlabs with aws polly
            # voice = user.get_voices_by_name(host_voice[key])[0]
            # audio_bytes = voice.generate_audio_bytes(value)
            print(key, value)
            audio_bytes = convert_to_speech_eleven(host_voice[key], value)
        return bytes_to_audio_segment(audio_bytes)


def generate_podcast(topic_with_google_search_results, original_prompt, duration=60):
    if duration:
        TOTAL_PARTS = min(max(1, duration // 10), 3)
    print("Total Parts:", TOTAL_PARTS)
    print("Total Parts Per Section:", PARTS_PER_SECTION)
    print("Generating podcast on %s" % (original_prompt))
    print("Generating Podcast Hosts")
    character_prompt = f"""
    Generate the names and descriptions of 2 podcast personalities, 1 male and 1 female, for a podcast about {original_prompt}. 
    The podcast hosts are tasked with talking about the topic, the outline should cover all the sorts of interesting components.
    The hosts do not know much about the topic the user provided ({original_prompt}).
    They should be people are are not experts on the topic, but are interested in it.
    Do not include any periods (.) in their names (Such as Dr. or Mrs.). Spaces in their names are okay though.
    """
    character_raw = generate(character_prompt)

    character_names_prompt = f"""
    {character_raw} \n What are the names of the characters? Return them in a comma separated list without spaces."""
    character_names = generate(character_names_prompt)
    character_list = [s.strip() for s in character_names.split(",")]
    print(character_raw)

    print("Choosing Podcast Host Voices")

    host_voice = voice_choice(character_list)
    print(host_voice)

    print("Generating High-Level Podcast Outline")
    outline_prompt = f"""Write a {TOTAL_PARTS}-part outline for a podcast on {original_prompt} with headings in the format 
    \n 1. <section 1>\n 2. <section 2>\n 3. ... \n Do not include any subpoints for each numbered item.\n\n
    We did a google search on this topic and found the following results: \n
    {topic_with_google_search_results if topic_with_google_search_results != original_prompt else "NO RESULTS"}\n
    If you find any of these google search results useful, please include them in your outline. \n

    The podcast hosts are tasked with talking about the topic, the outline should cover all the sorts of interesting components.
    The podcast hosts are not necessarily familiar with the topic.
    about the topic the user provided ({original_prompt}). \n
    Every outline part must be 1 and only 1 full sentence, specifying the content covered in that part of the podcast in complex detail.
    The podcast hosts have no ability to talk with anyone else on the show, so do not assume they will be interviewing anyone.
    The first part should include high-level overview of the podcast with a brief introudction of the hosts, {character_raw}
    """
    print("outline_prompt ", outline_prompt)
    outline_raw = generate(outline_prompt)
    print("outline_raw ", outline_raw)
    outline_list = []
    for i in outline_raw.split("\n"):
        try:
            outline_list.append(i.split(". ")[1].strip())
        except:
            pass
    print("Outline:", outline_list)

    print("Generating Outline Subsections")
    subsections = []
    for section in outline_list:
        outline_subsection_prompt = """
                Write a %s-part subsection outline for a podcast on %s with outline %s where this particular subsection is on %s. 
                ONLY include content specific to this particular subsection on %s. with headings in the format \n 1. <section 1>\n 2. <section 2>\n 3. ... \n Do not include any subpoints for each numbered item.\n\n
                Make sure the section addresses content that is unique to its part of the podcast. \n
                Every subsection outline part must be a full sentence, specifying the content covered in that part of the podcast in complex detail. 
                Be incredibly creative, technically accurate and piercing with insight.
                The podcast hosts have no ability to talk with anyone else on the show, and only the hosts will be talking together, 
                so do not assume they will be interviewing anyone.
                """ % (
            str(PARTS_PER_SECTION),
            original_prompt,
            "\n".join(outline_list),
            section,
            section,
        )
        subsection_raw = generate(outline_subsection_prompt)
        subsection_list = []
        for i in subsection_raw.split("\n"):
            try:
                subsection_list.append(i.split(". ")[1].strip())
            except:
                pass
        subsections.append(subsection_list)
        print(section, subsection_list)

    print("Compiling Outline")
    overall_outline = []
    for section in subsections:
        for subsection in section:
            overall_outline.append(subsection)
    outline_text = "\n".join(overall_outline)

    print("overall_outline", overall_outline)

    print("Generating Podcast Dialogue")
    overall_podcast = []
    podcast_transcript = ""
    for index, subsection in enumerate(overall_outline):
        # Construct transcript quickly
        podcast_transcript = ""
        for subsection_i in overall_podcast:
            for dialogue_snippet in subsection_i:
                podcast_transcript += dict_to_string(dialogue_snippet) + '\n'
        
        # For this subsection, generate dialogue
        prompt = f"""
        You are tasked with generating dialogue for a podcast that the user has requested about {original_prompt} with outline {outline_text} 
        where this particular subsection is on {subsection}. 
        ONLY include content specific to this particular subsection on {subsection}. \n
        We did a google search on this topic and found the following results: \n
        {topic_with_google_search_results}\n
        If any of the results are relevant, please include them in the dialogue you generate. \n
        The transcript of the podcast so far is: \n<Transcript Start>\n {podcast_transcript}. \n <Transcript End> \n
        The outline of the overall podcast is:\n<Outline Start>\n {outline_text}. \n <Outline End> \n
        Write a detailed, conflict rich, emotionally extreme set of podcast interactions on {subsection},
        including gripping dialogue, in a style that is emotionally captivating. Be creative.\n
        Make sure the podcast addresses content that is unique to its part of the outline, {subsection}.
        Do not focus on content addressed elsewhere in the outline. \n
        Do not include any headings or subheadings. \n
        The podcast hosts are {', '.join(character_list)}. Have them take turns arguing with each other on the topic.
        The podcast hosts have no ability to talk with anyone else on the show,
          so do not assume they will be interviewing anyone.
        {"This is the start of the podcast, so make sure the speakers introduce themselves" if index == 0 else ""}
        {"This is the end of the podcast, so make sure the speakers wrap up the podcast at the end" if index == len(overall_outline) - 1 else ""}
        The speakers must go back and forth at least 4 times.
        Generate more than 100 tokens.
        Generate less than 800 tokens.
        Add XML tags surrounding each speaker's text.
        """
        for i, name in enumerate(character_list):
            prompt += f"<Speaker {i+1}>{name}: <dialogue from {name}></Speaker {i+1}>\n"
        print("prompt", prompt)
        print("Generating dialogue for subsection %s of %s" % (index, len(overall_outline)))
        dialogue = generate(prompt)
        parsed_text_sequence = parse_podcast_text_sequence(dialogue)
        filtered_list = [
            d
            for d in parsed_text_sequence
            if any(key in character_list for key in d.keys())
        ]
        overall_podcast.append(filtered_list)

    dialogue_list = []
    for subsection in overall_podcast:
        for dialogue_snippet in subsection:
            dialogue_list.append(dialogue_snippet)

    audio_segments = []
    print(f"Generating audio from {len(dialogue_list)} dialogue snippets...")
    for index, dialogue in enumerate(dialogue_list):
        print(f"Generating audio for dialogue {index} of {len(dialogue_list)}...")
        print("Dialogue:", dialogue)
        audio_segments.append(dict_to_audio(dialogue, host_voice))
    combined_audio_segment = sum(audio_segments)

    # Convert user_text to snake case file name
    filename = original_prompt[:30].lower().replace(" ", "_")
    combined_audio_segment.export(f"output/{filename}.mp3", format="mp3")
    combined_audio_segment.export(f"output/speech.mp3", format="mp3")
    return f"output/{filename}.mp3"

def gen_once(text):
    return generate_podcast(text, text, duration=1)

if __name__ == "__main__":
    gen_once("Funny sloths")
    # x = bytes_to_audio_segment(synthesize_speech('Joanna', 'Hello World'))

    # x.export('test.mp3', format='mp3')