import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  # This imports the musicLibrary.py file

import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "give your api key "

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="enter your api key")

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
              {"role": "user", "content": command}]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]  # Get the song name after 'play'
        
        # Check if song exists in the music library
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Now playing {song}")
        else:
            speak("Sorry, I couldn't find that song in the library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Nova...")

    while True:
        # Recognize the wake word "Nova"
        r = sr.Recognizer()
        print("Listening for wake word...")

        try:
            with sr.Microphone() as source:
                print("Please say 'Nova' to activate.")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print(f"Detected word: {word}")

            if word.lower() == "nova":
                speak("Yes, I'm here! How can I assist you?")
                
                # Now listen for the command
                with sr.Microphone() as source:
                    print("Nova is active. Listening for command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(f"Command received: {command}")
                    
                    processCommand(command)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
        except Exception as e:
            print(f"Error: {e}")