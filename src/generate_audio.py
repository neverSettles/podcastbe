# User prompt in.
# Characters Out. Names + Descriptions.
# Characters + Users -> Outline.
# Characters + Users + Outline -> Sub-Outlines.
# Recursively Process Outline, section by section, passing in the existing text.

import random
import re
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from elevenlabslib import *
import numpy as np
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import boto3

load_dotenv()


TOTAL_PARTS = 2
PARTS_PER_SECTION = 1
MIN_HOSTS = 2
MAX_HOSTS = 2

api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic = Anthropic(
    api_key=api_key,
)

eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
user = ElevenLabsUser(eleven_labs_api_key)


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
        "Matthew",
    ]

    female_voices = [
        "Joanna",
    ]

    host_voice = {}
    for host in host_list:
        gender = get_gender(host)
        if gender == "Male":
            host_voice[host] = male_voices[random.randint(0, len(male_voices) - 1)]
        else:
            host_voice[host] = female_voices[random.randint(0, len(female_voices) - 1)]
    return host_voice


def generate_podcast(user_text, original_prompt):
    print("Generating podcast on %s" % (user_text))
    print("Generating Podcast Hosts")
    character_count = str(random.randint(MIN_HOSTS, MAX_HOSTS))
    character_prompt = f"""
    Generate the names and descriptions of 2 podcast personalities, 1 male and 1 female, for a podcast about {original_prompt}.
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
    outline_prompt = f"""Write a {TOTAL_PARTS}-part outline for a podcast on {original_prompt} with headings in the format \n 1. <section 1>\n 2. <section 2>\n 3. ... \n Do not include any subpoints for each numbered item.\n\n
    Every outline part must be a full sentence, specifying the content covered in that part of the podcast in complex detail.
    The first part should include high-level overview of the podcast with a brief introudction of the hosts, {character_raw}
    """
    outline_raw = generate(outline_prompt)
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
                Write a %s-part subsection outline for a podcast on %s with outline %s where this particular subsection is on %s. ONLY include content specific to this particular subsection on %s. with headings in the format \n 1. <section 1>\n 2. <section 2>\n 3. ... \n Do not include any subpoints for each numbered item.\n\n
                Make sure the section addresses content that is unique to its part of the podcast. \n
                Every subsection outline part must be a full sentence, specifying the content covered in that part of the podcast in complex detail. Be incredibly creative, technically accurate and piercing with insight.
                If this is the introduction, make sure to include at least a subsection for a broad introduction, and a subsection introducing the hosts.
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

    print("Generating Podcast Dialogue")
    overall_podcast = []
    podcast_transcript = ""
    for subsection in overall_outline:
        podcast_transcript = ""
        for subsection_i in overall_podcast:
            for dialogue_snippet in subsection_i:
                podcast_transcript += dict_to_string(dialogue_snippet)
        prompt = f"""
        The transcript of the podcast so far is: \n<Transcript Start>\n {podcast_transcript}. \n <Transcript End> \n
        The outline of the overall podcast is:\n<Outline Start>\n {outline_text}. \n <Outline End> \n
        Write a detailed, conflict rich, emotionally extreme set of podcast interactions on {subsection}, including gripping dialogue, in a style that is emotionally captivating. Be creative.\n
        Make sure the podcast addresses content that is unique to its part of the outline, {subsection}. Do not focus on content addressed elsewhere in the outline. \n
        Do not include any headings or subheadings. \n
        The podcast hosts are {', '.join(character_list)}. Have them take turns addressing one another.
        If this is the first section, make sure to provide a high-level overview and introduce the hosts.
        This section is likely in the middle of the podcast, so do not start or end the podcast.
        The speakers must go back and forth at least 4 times.
        Generate more than 100 tokens.
        Add XML tags surrounding each speaker's text.
        """
        for i, name in enumerate(character_list):
            prompt += f"<Speaker {i+1}>{name}: <dialogue from {name}></Speaker {i+1}>\n"
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
    
    def synthesize_speech(voice, text):
        # Create a client using your AWS access keys stored as environment variables
        polly_client = boto3.Session(
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                        region_name=os.getenv('AWS_REGION', 'us-east-1')).client('polly')

        response = polly_client.synthesize_speech(
            VoiceId=voice,
            OutputFormat='mp3',
            Engine='neural',
            Text=text
        )

        # Assuming you've already made the request and have the response
        audio_stream = response['AudioStream']
        return audio_stream.read()

    def dict_to_audio(dialogue_dict, filename="audio"):
        string = ""
        for key, value in dialogue_dict.items():
            string += f"{key}: {value} "
            # replace elevenlabs with aws polly
            # voice = user.get_voices_by_name(host_voice[key])[0]
            # audio_bytes = voice.generate_audio_bytes(value)
            audio_bytes = synthesize_speech(host_voice[key], value)
        return bytes_to_audio_segment(audio_bytes)

    def combine_audio_segments(audio_segments):
        return sum(audio_segments)

    audio_segments = []
    print(f"Generating audio from {len(dialogue_list)} dialogue snippets...")
    for index, dialogue in enumerate(dialogue_list):
        print(f"Generating audio for dialogue {index} of {len(dialogue_list)}...")
        print("Dialogue:", dialogue)
        audio_segments.append(dict_to_audio(dialogue))
    combined_audio_segment = combine_audio_segments(audio_segments)

    # Convert user_text to snake case file name
    filename = original_prompt[:30].lower().replace(" ", "_")
    combined_audio_segment.export(f"output/{filename}.mp3", format="mp3")
    combined_audio_segment.export(f"output/speech.mp3", format="mp3")
    return f"output/{filename}.mp3"

def gen_once(text):
    return generate_podcast(text, text)

if __name__ == "__main__":
    gen_once("How the cross ocean internet cable was laid")