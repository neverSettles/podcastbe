import boto3
import os
import pyaudio
import io

from pydub import AudioSegment
from pydub.playback import play

def synthesize_speech(text):
    # Create a client using your AWS access keys stored as environment variables
    polly_client = boto3.Session(
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')).client('polly')

    response = polly_client.synthesize_speech(
        VoiceId='Matthew',
        OutputFormat='mp3',
        Engine='neural',
        Text=text
    )

    # Assuming you've already made the request and have the response
    audio_stream = response['AudioStream']

    # Save the audio stream to a file
    file_name = "output.mp3"
    with io.open(file_name, 'wb') as audio_file:
        audio_file.write(audio_stream.read())
        print("Speech synthesis completed. The output is stored as speech.mp3")

    # Play the audio file using pydub
    audio = AudioSegment.from_mp3(file_name)
    play(audio)

    # Upload file to S3 bucket
    s3 = boto3.resource('s3',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                        region_name=os.getenv('AWS_REGION', 'us-east-1'))

    s3.Bucket('speechtotextchris').put_object(Key='speech.mp3', Body=audio_stream.getvalue())
    print("File uploaded to S3 bucket 'texttospeechchris' as 'speech.mp3'")

if __name__ == "__main__":
    synthesize_speech(
    """
Host: Welcome to "The Bay Area Chronicles," the podcast where we explore the stories and experiences of individuals living in the vibrant Bay Area. I'm your host, and today we have a fascinating tale to share. Joining us is Krishna, an Indian software engineer who has been facing a unique challenge in his quest for love. Welcome, Krishna!

Krishna: Thank you for having me. It's great to be here.

Host: So, Krishna, tell us a bit about yourself and your journey as a software engineer in the Bay Area.

Krishna: Well, I moved to the Bay Area a few years ago to pursue my career in software engineering. It's been an incredible experience professionally, but on a personal level, it has been quite challenging. You see, there's a significant gender imbalance here, with a surplus of men and a scarcity of women. This makes it difficult to find a girlfriend and establish meaningful connections.

"""
)