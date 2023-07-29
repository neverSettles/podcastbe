import boto3
import os

def synthesize_speech(text):
    # Create a client using your AWS access keys stored as environment variables
    polly_client = boto3.Session(
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')).client('polly')

    response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = text)

    # The response body contains the audio stream.
    # Writing the stream in a mp3 file
    with open('speech.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    
    print("Speech synthesis completed. The output is stored as speech.mp3")

synthesize_speech('Hello, how can I assist you today?')