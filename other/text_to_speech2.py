from google.cloud import texttospeech

# Create a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="Hello, world!")

# Build the voice request
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    name="en-US-Wavenet-F"
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# Write the response to the output file.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)