import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def synthesize_text_with_api_key(input_content, output_filename, input_type="text", voice_name='en-US-Neural2-F', language_code="en-US"):
    api_key = os.getenv("GOOGLE_TTS_API_KEY")
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"

    headers = {
        'Content-Type': 'application/json',
    }

    # Decide whether the input is SSML or text based on input_type
    if input_type == "ssml":
        input_data = {'ssml': input_content}
    else:
        input_data = {'text': input_content}

    body = {
        'input': input_data,
        'voice': {
            'languageCode': language_code,
            'name': voice_name,
            'ssmlGender': 'FEMALE'
        },
        'audioConfig': {
            'audioEncoding': 'Linear16'
        }
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        audio_content = response.json().get('audioContent', None)
        if audio_content:
            with open(output_filename, 'wb') as out:
                out.write(base64.b64decode(audio_content))
                print(f"Audio content written to '{output_filename}'")
        else:
            print("No audio content found in response")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Plain text example
text_input = "Hello from Google Cloud Text-to-Speech using plain text!"
synthesize_text_with_api_key(text_input, "output_text.mp3", voice_name='en-US-Studio-O', language_code="en-US")

# SSML example
ssml_input = """<speak><emphasis level="strong">Hello</emphasis> from Google Cloud Text-to-Speech using SSML!</speak>"""
ssml_input = """<speak>
    <p>In the heart of a vibrant city, there was a young girl named Cait. Every night, she clutched her favorite stuffed animal, a sloth named <phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme>.</p>

    <p><emphasis level="moderate">"<phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme>,"</emphasis> Cait whispered one evening, her eyes filled with wonder, <emphasis level="moderate">"do you ever wish you could come to life and take me on an adventure?"</emphasis></p>
    
    <p>To Cait's surprise, <phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme>'s eyes twinkled. In a soft, slow voice, he replied, <emphasis level="moderate">"Oh, Cait. If I could, I would show you the magical treetops of the rainforest where real sloths live."</emphasis></p>

    <p>As Cait closed her eyes, the room began to transform. The sounds of traffic faded away, replaced by the distant call of exotic birds and the gentle rustling of leaves.</p>

    <p>When she opened her eyes, Cait found herself high up in a giant treehouse. <phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme> was beside her, but he was now as big as her! <emphasis level="strong"><phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme>!</emphasis> Cait exclaimed, hugging her friend. <emphasis level="moderate">"This is amazing!"</emphasis></p>

    <p><phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme> chuckled, <emphasis level="moderate">"Welcome to my world, Cait."</emphasis> He took her by the hand, and together, they explored the enchanted forest. They met colorful birds, playful monkeys, and even other friendly sloths.</p>
    
    <p>As the moon began to rise, <phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme> led Cait to a cozy nook in the treehouse. There, they shared stories and giggled under the soft light of fireflies.</p>

    <p><emphasis level="moderate"><phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme>,</emphasis> Cait whispered as her eyelids grew heavy, <emphasis level="moderate">"thank you for this magical night."</emphasis></p>
    
    <p><phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme> hugged her tight, <emphasis level="moderate">"Remember, Cait. Even in the heart of the city, magic is just a dream away."</emphasis></p>

    <p>With those words, Cait drifted off to sleep, <phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme> back in his regular stuffed form by her side.</p>

    <p>The next morning, Cait woke up in her own bed, the sounds of the city outside her window. But on her nightstand, there lay a single, beautiful feather, a gentle reminder of the magical adventure she had with her beloved <phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme>.</p>

    <p>And so, each night, Cait drifted off to sleep, knowing that with <phoneme alphabet="ipa" ph="slɔː.θi">Slothy</phoneme> by her side, every dream could become an adventure.</p>
</speak>

"""
synthesize_text_with_api_key(ssml_input, "output_ssml.mp3", input_type="ssml", voice_name='en-US-Neural2-F', language_code="en-US")
