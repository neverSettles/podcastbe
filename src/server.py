import openai
import os
import boto3
from botocore.exceptions import NoCredentialsError

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv

from gen_podcast import create_podcast
from gen_podcast import create_emotional_podcast

# Set up OpenAI API credentials
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)
s3 = boto3.client('s3')

def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

def bucket_exists(bucket_name):
    s3 = boto3.resource('s3')
    return s3.Bucket(bucket_name) in s3.buckets.all()

def ensure_bucket_exists(bucket_name, region=None):
    if not bucket_exists(bucket_name):
        return create_bucket(bucket_name, region)
    else:
        print(f"Bucket {bucket_name} already exists.")
        return True

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Call /generate to generate a podcast!"})

def append_text_to_s3_file(bucket, key, text):
    # Download the file to a local file
    s3.meta.client.download_file(bucket, key, '/tmp/logfile.txt')

    # Append to the file
    with open('/tmp/logfile.txt', 'a') as file:
        file.write(text)

    # Upload the file back to S3
    s3.meta.client.upload_file('/logfile.txt', bucket, key)

def try_append(text):
    try:
        ensure_bucket_exists('podcast-generator')
        key = 'logfile.txt'
        append_text_to_s3_file('podcast-generator', key, text)
    except: 
        pass

@app.route('/generate', methods=['POST'])
def create_post():
    data = request.get_json()  # parse parameters from incoming request

    topic = data.get('topic')  # get parameter called 'topic'
    duration = data.get('duration')  # get parameter called 'duration'
    tone = data.get('tone')  # get parameter called 'tone'
    
    if "emotional" in tone.lower():
        url = create_emotional_podcast(topic, duration, tone)
        try_append( "\n" + topic + "\n" + str(duration) + "\n" + tone + "\n" + url + "\n")
        return jsonify({"share_url": url}), 200
    else:
        create_podcast(topic, duration, tone)
        # Upload to S3
        try:
            ensure_bucket_exists('podcast-generator')
            s3.upload_file('./output/speech.mp3', 'podcast-generator', 'speech.mp3')
            print("Upload Successful")
            url = s3.generate_presigned_url('get_object', Params={'Bucket': 'podcast-generator', 'Key': 'speech.mp3'}, ExpiresIn=3600)
            print(url)
            try_append( "\n" + topic + "\n" + str(duration) + "\n" + tone + "\n" + url + "\n")

            return jsonify({"url": url}), 200
            
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")


@app.route('/generate/demo', methods=['POST'])
def create_post_demo():
    data = request.get_json()  # parse parameters from incoming request

    topic = data.get('topic')  # get parameter called 'topic'
    duration = data.get('duration')  # get parameter called 'duration'
    tone = data.get('tone')  # get parameter called 'tone'
    
    transcript = create_podcast(topic, duration, tone)
    return send_file('../output/speech.mp3', mimetype="audio/mp3"), 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
