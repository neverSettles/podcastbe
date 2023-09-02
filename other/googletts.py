import requests
import base64
import os
from dotenv import load_dotenv
import time, os, requests, base64

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
            'name': voice_name
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


text_input = """
“लाइफ असल में चीज़ो को hold करने और फिर सही समय आने पर उन्हें जाने देने का ही नाम है”-- Zen फिलोसोफी का एक जाना माना कथन 

ये बात कितनी सही है! बचपन से जवानी तक हर इंसान अपना जीवन कुछ बड़ा करने में लगाता है। इस journey में उसे कई सारी चीज़े experience करने का मौका मिलता है। ये बात सच है कि हर एक moment अपने साथ एक नया रंग लेकर आता है और काफी बार हम उसे अच्छे से एक्सेप्ट करते हैं। लेकिन इसके साथ ये भी सच है कि life में कोई भी चीज़ permanent नहीं होती। हर एक चीज़ को कभी न कभी अपने निर्धारित समय पर जाना ही होता है, फिर चाहे वो रिश्ते हो या कोई particular जगह, ये philosophy हर एक element के लिए सच साबित होती है। वैसे आपको पता ही होगा कि हमेशा से ही दुनिया में अलग-अलग प्लेसेस पर different philosophies का importance रहा है। ancient philosophies और school ऑफ़ thoughts हमेशा से ही समाज को एक बेहतर position में place करने में हेल्पफुल रहे हैं। आपने खुद भी अपने चारों ओर काफी सारी ऐसी practices के बारे में सुना होगा जो इससे मेल खाती है। लेकिन क्या आपने कभी Zen नाम की philosophy और उसके elements के बारे में सुना है? अगर आपका जवाब हाँ है तो आप एक extraordinary art को पहले से ही कुछ हद तक appreciate करते होंगे और जिन्होंने इसके बारे में नहीं सुना, उनको भी चिंता करने की ज़रूरत नहीं है। इस स्पेशल episodic journey में हम इसी महान philosophy के बारे में detail से जानेंगे और समझेंगे कि कैसे ये आज भी हमारी लाइफ में relevance रखती है। तो आइये शुरू करते हैं!

"""
synthesize_text_with_api_key(text_input, "hindi/hindiA.mp3", voice_name='hi-IN-Neural2-A', language_code="hi-IN")
synthesize_text_with_api_key(text_input, "hindi/hindiB.mp3", voice_name='hi-IN-Neural2-B', language_code="hi-IN")
synthesize_text_with_api_key(text_input, "hindi/hindiC.mp3", voice_name='hi-IN-Neural2-C', language_code="hi-IN")
synthesize_text_with_api_key(text_input, "hindi/hindiD.mp3", voice_name='hi-IN-Neural2-D', language_code="hi-IN")
