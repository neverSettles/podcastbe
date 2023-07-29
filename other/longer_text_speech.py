import boto3
import os
import pyaudio
import io

def synthesize_speech(text):
    # Create a client using your AWS access keys stored as environment variables
    polly_client = boto3.Session(
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')).client('polly')

    response = polly_client.synthesize_speech(VoiceId='Matthew',
                OutputFormat='mp3', 
                Text = text)

    # The response body contains the audio stream. We will save it in a byte stream
    # so we can use it multiple times.
    audio_stream = io.BytesIO(response['AudioStream'].read())

    # Writing the stream in a mp3 file
    filename = 'speech.mp3'
    with open(filename, 'wb') as file:
        file.write(audio_stream.getvalue())
    print("Speech synthesis completed. The output is stored as speech.mp3")

    # Upload file to S3 bucket
    s3 = boto3.resource('s3',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                        region_name=os.getenv('AWS_REGION', 'us-east-1'))

    s3.Bucket('texttospeechchris').put_object(Key='speech.mp3', Body=audio_stream.getvalue())
    print("File uploaded to S3 bucket 'texttospeechchris' as 'speech.mp3'")

    # Play the audio file using pyaudio
    p = pyaudio.PyAudio()
    chunk = 1024
    audio_stream.seek(0)  # Rewind the audio stream to the beginning
    stream = p.open(format=p.get_format_from_width(2), channels=1, rate=22050, output=True)
    data = audio_stream.read(chunk)

    while data:
        stream.write(data)
        data = audio_stream.read(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
synthesize_speech(
    """
Host: Welcome to "The Bay Area Chronicles," the podcast where we explore the stories and experiences of individuals living in the vibrant Bay Area. I'm your host, and today we have a fascinating tale to share. Joining us is Krishna, an Indian software engineer who has been facing a unique challenge in his quest for love. Welcome, Krishna!

Krishna: Thank you for having me. It's great to be here.

Host: So, Krishna, tell us a bit about yourself and your journey as a software engineer in the Bay Area.

Krishna: Well, I moved to the Bay Area a few years ago to pursue my career in software engineering. It's been an incredible experience professionally, but on a personal level, it has been quite challenging. You see, there's a significant gender imbalance here, with a surplus of men and a scarcity of women. This makes it difficult to find a girlfriend and establish meaningful connections.

Host: That's certainly a unique predicament. Can you elaborate on how this gender imbalance has affected your dating life?

Krishna: Absolutely. The gender ratio in the Bay Area skews heavily towards men, especially in the tech industry. This means that the dating pool is significantly smaller for men like me. It's not just about the numbers; it's also about the dynamics. The competition is fierce, and it can be overwhelming at times. It's challenging to stand out and make a genuine connection when there are so many other men vying for the same attention.

Host: That sounds incredibly tough. Have you tried any strategies or approaches to navigate this dating landscape?

Krishna: Oh, definitely. I've tried various avenues, from online dating apps to attending social events and meetups. While these platforms provide opportunities to meet new people, it's still challenging to find someone who shares a genuine connection. It often feels like a numbers game, and it can be disheartening.

Host: I can imagine. So, what keeps you motivated to continue your search for love despite these obstacles?

Krishna: It's all about staying positive and keeping an open mind. I believe that the right person is out there, and I refuse to let the odds discourage me. I focus on personal growth, pursuing my passions, and building a fulfilling life outside of dating. By doing so, I hope to attract someone who appreciates me for who I am.

Host: That's an inspiring perspective, Krishna. Before we wrap up, do you have any advice for others who might be facing similar challenges?

Krishna: Absolutely. My advice would be to stay true to yourself and not let the circumstances define your worth. It's essential to focus on personal growth, pursue your passions, and surround yourself with a supportive community. Remember that finding love is a journey, and it's important to enjoy the process rather than solely focusing on the outcome.

Host: Wise words, Krishna. Thank you so much for sharing your story and insights with us today. We wish you all the best in your search for love.

Krishna: Thank you for having me. It was a pleasure being here.
"""
)