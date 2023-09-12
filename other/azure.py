import requests
import os
from pydub import AudioSegment
from pydub.playback import play

# Define your Azure Text-to-Speech API key and region.
SUBSCRIPTION_KEY = 'YOUR_API_KEY'
REGION = 'YOUR_SERVICE_REGION'

# Define API endpoint and headers.
TTS_ENDPOINT = f'https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1'
HEADERS = {
    'Authorization': f'Bearer {SUBSCRIPTION_KEY}',
    'Content-Type': 'application/ssml+xml',
    'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
    'User-Agent': 'YOUR_APP_NAME'
}

# Define your SSML input (used for advanced speech formatting).
SSML = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-Guy24kRUS">Hello, this is a test of Azure Text to Speech service.</voice>
</speak>
"""

# Request audio from Azure TTS API.
response = requests.post(TTS_ENDPOINT, headers=HEADERS, data=SSML)

# Check if the request was successful.
if response.status_code == 200:
    # Save the response audio to a file.
    with open('output.wav', 'wb') as audio_file:
        audio_file.write(response.content)
    
    # Play the audio.
    audio = AudioSegment.from_wav('output.wav')
    play(audio)

else:
    print(f"Failed with status code {response.status_code}. Response: {response.text}")
