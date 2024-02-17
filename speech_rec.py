import speech_recognition as sr
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio 

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to capture audio and recognize speech
async def recognize_speech():
    with sr.Microphone() as source:
        recognizer.energy_threshold = 1000
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Adjusted for background noise")

        try:
            print("Listening for input: ")
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=10)

            # save audio as an wav file
            with open("microphone-results.wav", "wb") as f:
                f.write(audio.get_wav_data())
            # recognizer.recognize_google(audio)

            media_file = open('microphone-results.wav', 'rb')

            client = OpenAI()
            text = client.audio.transcriptions.create(
                model='whisper-1',
                file=media_file,
                response_format='json'
            )
            return (text.text)
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period")
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Error fetching results; {e}")