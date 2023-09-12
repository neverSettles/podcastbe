import requests
import base64
import os
from dotenv import load_dotenv
from pydub import AudioSegment
import io

load_dotenv()

def synthesize_text_with_api_key(input_content, input_type="text", voice_name='en-US-Neural2-F', language_code="en-US"):
    api_key = os.getenv("GOOGLE_TTS_API_KEY")
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"

    headers = {
        'Content-Type': 'application/json',
    }

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
            audio_segment = AudioSegment.from_file(io.BytesIO(base64.b64decode(audio_content)), format="wav")
            return audio_segment
        else:
            print("No audio content found in response")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def chunk_text(text, max_bytes=5000):
    chunks = []
    while len(text.encode('utf-8')) > max_bytes:
        limit = min(len(text) - 1, max_bytes)
        while limit > 0 and (len(text[:limit].encode('utf-8')) > max_bytes or text[limit] not in (' ', '\n', '.', '!', '?')):
            limit -= 1
        if limit == 0:  # If no suitable break found within max_bytes, force a chunk split
            # Find the maximum bytes without breaking a multi-byte character
            byte_limit = max_bytes
            while byte_limit > 0 and text.encode('utf-8')[byte_limit] & 0xC0 == 0x80:
                byte_limit -= 1
            limit = len(text[:byte_limit].encode('utf-8').decode('utf-8'))
        chunks.append(text[:limit])
        text = text[limit:].lstrip()
    if text:
        chunks.append(text)
    return chunks

def gen_audio(text, filename, voice_name, language_code):
    chunks = chunk_text(text)
    combined_audio = AudioSegment.empty()
    for chunk in chunks:
        audio_segment = synthesize_text_with_api_key(chunk, None, voice_name=voice_name, language_code=language_code)
        if audio_segment:
            combined_audio += audio_segment

    combined_audio.export(filename, format="mp3")


def main(text, filename, voice_name, language_code):
    gen_audio(text, filename, voice_name, language_code)
    print(f"Combined audio exported to '{filename}'")

if __name__ == "__main__":
    text_input = """
Episode 1- The Origins

“लाइफ असल में चीज़ो को hold करने और फिर सही समय आने पर उन्हें जाने देने का ही नाम है”-- Zen फिलोसोफी का एक जाना माना कथन 

ये बात कितनी सही है! बचपन से जवानी तक हर इंसान अपना जीवन कुछ बड़ा करने में लगाता है। इस journey में उसे कई सारी चीज़े experience करने का मौका मिलता है। ये बात सच है कि हर एक moment अपने साथ एक नया रंग लेकर आता है और काफी बार हम उसे अच्छे से एक्सेप्ट करते हैं। लेकिन इसके साथ ये भी सच है कि life में कोई भी चीज़ permanent नहीं होती। हर एक चीज़ को कभी न कभी अपने निर्धारित समय पर जाना ही होता है, फिर चाहे वो रिश्ते हो या कोई particular जगह, ये philosophy हर एक element के लिए सच साबित होती है। वैसे आपको पता ही होगा कि हमेशा से ही दुनिया में अलग-अलग प्लेसेस पर different philosophies का importance रहा है। ancient philosophies और school ऑफ़ thoughts हमेशा से ही समाज को एक बेहतर position में place करने में हेल्पफुल रहे हैं। आपने खुद भी अपने चारों ओर काफी सारी ऐसी practices के बारे में सुना होगा जो इससे मेल खाती है। लेकिन क्या आपने कभी Zen नाम की philosophy और उसके elements के बारे में सुना है? अगर आपका जवाब हाँ है तो आप एक extraordinary art को पहले से ही कुछ हद तक appreciate करते होंगे और जिन्होंने इसके बारे में नहीं सुना, उनको भी चिंता करने की ज़रूरत नहीं है। इस स्पेशल episodic journey में हम इसी महान philosophy के बारे में detail से जानेंगे और समझेंगे कि कैसे ये आज भी हमारी लाइफ में relevance रखती है। तो आइये शुरू करते हैं!

हमारे सामने सबसे पहला सवाल खड़ा होता है कि आखिर ये Zen है क्या? अगर हम simply इस शब्द की बात करे तो इसका मतलब है ultimate reality; हमारे expression का एक  ऐसा फॉर्म जिसमे हम खुद को moment by moment एक्सप्रेस करते हैं और एक disciplined practice को अपनाने हैं। ये disciplined activity अक्सर meditation की फॉर्म में अपनाई जाती है जिससे हम चीज़ो के true nature को समझ पाते हैं।
Zen को dominantly Mahayana Buddhism का एक important एलिमेंट माना जाता है जो कि China में originate हुआ था. Zen शब्द middle Chinese वर्ड Chan के Japanese pronunciation से लिया गया है जो कि खुद Sanskrit शब्द ‘ध्यान’ का translation हैं। 

Zen में काफी सारी practices को promote किया जाता है जैसे self-restraint यानी खुद पर काबू रखना, meditation practice यानी ध्यान लगाना, खुद के mind के नेचर को अच्छे से समझना और साथ ही साथ दूसरी चीज़ो के nature को भी समझना जिसमे arrogrance या ego की कोई जगह न हो। क्या आपके मन में कुछ और भी आ रहा है? ज़रूर कभी न कभी आपके घर में बड़े-बुज़ुर्गों ने आपसे इन सब mindfulness की activities को करने को बोला ही होगा। और आपको जानकार हैरानी होगी दोस्तों कि इस शो के माध्यम से हम भी Zen philosophy और इंडियन spiritual traditions की similarities को discuss करेंगे। ये activities अक्सर दूसरे लोगों के भले के लिए यूज़ की जाती है और खुद का एक personal एक्सप्रेशन माना जाता है। जैसे कि हमने पहले भी समझा था, ये किसी sutra की knowledge के साथ अकेले नहीं चलता बल्कि इस philosophy में spiritual practice की direct understanding होती है जो कि अक्सर किसी accomplished master के ज़रिये achieve की जाती है जो पहले से इस आर्ट में माहिर हो। हम समझेंगे कि कैसे Zen और इंडियन स्कूल ऑफ़ thought connected है और हमें एक बेहतर लाइफ जीने के लिए motivate करता है।  


मॉडर्न टाइम में इस प्रैक्टिस को कई सारे elements को साथ जोड़कर perform किया जाता है जैसे scriptures को पढ़ना, अच्छे कर्म करना, किसी समारोह में पार्ट लेना, image worship की practice और meditation को सच्चे मन से करना। Modern टाइम्स में Zen philosophy हमें कई सारी चीज़ो को tackle करने में मदद कर सकती है। इसका सबसे बड़ा example है कि आज की fast-paced lifestyle में Zen philosophy हमें अपने emotional वेल-बीइंग को अच्छा रखने में हेल्प कर सकती है और ये तो केवल इसकी शुरुआत है। इस philosophy के ऐसे कई सारे elements हैं जो अभी discuss करना बाकी है। आने वाले episodes में इसके और भी राज़ आपके लिए खोले जायेंगे लेकिन उसके लिए आपको हमारे साथ बने रहना होगा। तो क्या आप तैयार हैं? बने रहिये और सुनते रहिए KukuFM की इस ख़ास पेशकश को! """
 
    main(text_input, 'hindi/hindiA.mp3', voice_name='hi-IN-Neural2-A', language_code="hi-IN")
    main(text_input, 'hindi/hindiB.mp3', voice_name='hi-IN-Neural2-B', language_code="hi-IN")
    main(text_input, 'hindi/hindiC.mp3', voice_name='hi-IN-Neural2-C', language_code="hi-IN")
    main(text_input, 'hindi/hindiD.mp3', voice_name='hi-IN-Neural2-D', language_code="hi-IN")
