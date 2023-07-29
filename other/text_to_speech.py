from gtts import gTTS
import os

# Define your text
text_to_read = "Hello, this is a test for Google Text-to-Speech."

# Create a speech object
speech = gTTS(text=text_to_read, lang='en', slow=False)

# Save the speech audio into a file
speech.save("output.mp3")

# If you want to automatically play the file (on a system with mpg321 installed)
os.system("mpg321 output.mp3")
