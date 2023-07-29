import boto3
from contextlib import closing
import os

def save_speech_to_s3(text, bucket_name, filename):
    polly_client = boto3.Session(
        aws_access_key_id='<YOUR_ACCESS_KEY>',
        aws_secret_access_key='<YOUR_SECRET_KEY>',
        region_name='us-west-2'  # or any other AWS region you prefer
    ).client('polly')

    response = polly_client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        VoiceId='Joanna'
    )

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join("/tmp", filename)

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as ioe:
                print("IOError: " + str(ioe))
                return None

            s3_client = boto3.client('s3',
                                     aws_access_key_id='<YOUR_ACCESS_KEY>',
                                     aws_secret_access_key='<YOUR_SECRET_KEY>',
                                     region_name='us-west-2')

            s3_client.upload_file(output, bucket_name, filename)

            print(f"File saved as {filename} in {bucket_name} bucket.")
            return filename
    else:
        # The response didn't contain audio data, return None
        return None

save_speech_to_s3("Hello, this is a test.", 'texttospeechchris', 'test.mp3')