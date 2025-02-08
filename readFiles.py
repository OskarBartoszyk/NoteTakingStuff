from gtts import gTTS
import pygame
import os
import re

# Path to the text file you want to convert to speech
input_file = "..."

# Generate a file name for the audio output (without .md extension)
file_name = os.path.splitext(os.path.basename(input_file))[0] + ".mp3"

# Path to save the audio file
speach_folder = '/home/oskar/tasks/speach'
output_file = os.path.join(speach_folder, file_name)

# Language for text-to-speech
language = 'pl'

# Ensure the speech folder exists
if not os.path.exists(speach_folder):
    os.makedirs(speach_folder)

def clean_text(text):
    """Removes unwanted characters from the text."""
    cleaned_text = re.sub(r'[#\*\-]', '', text)  # Removes #, *, and -
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Removes extra whitespace
    return cleaned_text

# Read and clean the content of the text file
try:
    with open(input_file, 'r', encoding='utf-8') as file:
        raw_text = file.read()
        mytext = clean_text(raw_text)
except FileNotFoundError:
    print(f"Error: The file '{input_file}' does not exist.")
    exit(1)
except Exception as e:
    print(f"Error reading the file: {str(e)}")
    exit(1)

# Generate speech using gTTS

myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save(output_file)

# Play the audio using pygame
try:
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    # Wait until the audio playback finishes
    while pygame.mixer.music.get_busy():
        pass

    print("Audio playback completed.")
except Exception as e:
    print(f"Error during audio playback: {str(e)}")
    exit(1)
