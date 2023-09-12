from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

audio = speech.RecognitionAudio(uri="gs://your-bucket/your-audio-file.wav")