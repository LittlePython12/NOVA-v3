import sounddevice as sd
import speech_recognition as sr
import asyncio
import edge_tts
import os
from playsound import playsound
import webbrowser
import datetime
import requests
import time
import urllib.parse
import sys
import random
import subprocess


# --------------------------------
# CONSOLE ENCODING
# --------------------------------

sys.stdout.reconfigure(encoding="utf-8")

# --------------------------------
# CLASS CONFIGURATIONS
# --------------------------------

ASSISTANT_NAME = "Nova"
WAKE_WORDS = ["nova", "hey nova"]

VOICE = "en-GB-RyanNeural"
TEMP_AUDIO_FILE = "temp_output.mp3"

CITY = "Regina"
SAMPLE_RATE = 44100
DEFAULT_LISTEN_DURATION = 5
COMMAND_LISTEN_DURATION = 6


# --------------------------------
# VOICE SYSTEM USING EDGE-TTS
# --------------------------------

async def speak_async(text):
    print(f"{ASSISTANT_NAME}: {text}")

    try:
        # Delete old temp file if it exists
        if os.path.exists(TEMP_AUDIO_FILE):
           os.remove(TEMP_AUDIO_FILE)

        communicate = edge_tts.Communicate(text, VOICE)

        # Properly stream audio chunks into the mp3 file
        async for chunk in communicate.stream():
            if chunk ["type"] == "audio":
                with open(TEMP_AUDIO_FILE, "ab") as file:
                    file.write(chunk["data"])

        # Play the mp3 after it's done generating
        playsound(TEMP_AUDIO_FILE)

    except Exception as error:
        print(f"TTS Error: {error}")

    finally:
        # Clean up the temp file
        if os.path.exists(TEMP_AUDIO_FILE):
            try:
                os.remove(TEMP_AUDIO_FILE)
            except Exception:
                pass


def speak(text):
    asyncio.run(speak_async(text))



# --------------------------------
# BLOCK OF CODE FOR SPEECH RECOG.
# --------------------------------

def listen(duration=DEFAULT_LISTEN_DURATION):
    recognizer = sr.Recognizer()
    print("🎙 Listening...")

    try:
        audio_data = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )
        sd.wait()

        audio_bytes = audio_data.tobytes()
        audio = sr.AudioData(audio_bytes, SAMPLE_RATE, 2)

        query = recognizer.recognize_google(audio, language="en-US")
        query = query.lower()

        print(f"You said: {query}")
        return query

    except sr.UnknownValueError:
        print("No speech recognized.")
        return ""

    except sr.RequestError:
        print("Speech recognition service unavailable.")
        speak("Speech service is unavailable.")
        return ""

    except Exception as error:
        print(f"Listen Error: {error}")
        return ""

# --------------------------------
# HELPER FUNCTIONS
# --------------------------------
def contains_wake_word(phrase):
    return any(wake_word in phrase for wake_word in WAKE_WORDS)



def extract_command_from_phrase(phrase):
    for wake_word in WAKE_WORDS:
        if wake_word in phrase:
            return phrase.replace(wake_word, "").strip()
    return ""



def clean_weather_text(text):
    cleaned = text.strip()
    cleaned = cleaned.replace("°C", " degrees Celsius")
    cleaned = cleaned.replace("+", "plus ")
    cleaned = cleaned.replace("-", "minus ")
    return cleaned

# --------------------------------
# COMMAND ACTIONS
# --------------------------------
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")


def tell_date():
    current_date = datetime.datetime.now().strftime("%A, %B, %d, %Y")
    speak(f"Today is {current_date}")



def open_google():
    speak("Opening Google.")
    webbrowser.open("https://www.google.com")



def open_youtube():
    speak("Opening Youtube.")
    webbrowser.open("https://www.youtube.com")



def open_gmail():
    speak("Opening Gmail.")
    webbrowser.open("https://mail.google.com")



def open_github():
    speak("Opening Github.")
    webbrowser.open("https://www.github.com")



def open_spotify():
    speak("Opening Spotify.")
    webbrowser.open("https://open.spotify.com")



def search_google(query):
    if not query:
        speak("What would you like me to search for?")
        return

    safe_query = urllib.parse.quote(query)
    speak(f"Searching Google for {query}.")
    webbrowser.open(f"https://www.google.com/search?q={safe_query}")



def search_youtube(query):
    if not query:
        speak("What would you like me to search for on Youtube?")
        return

    safe_query = urllib.parse.quote(query)
    speak(f"Searching Youtube for {query}.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={safe_query}")



def get_weather():
    speak("Checking the weather.")

    try:
        url = f"https://wttr.in/{CITY}?format=Temperature:+%t,+Condition:+%C"
        response = requests.get(url, timeout = 5)

        weather_text = clean_weather_text(response.text)
        print(f"Weather response: {weather_text}")

        speak(f"The current weather in {CITY} is {weather_text}")

    except Exception as error:
        print(f"Weather error: {error}")
        speak("I couldn't fetch the weather right now.")


def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why did the developer go broke? Because he used up all his cache.",
        "I would tell you a UDP joke, but you might not get it.",
        "Why was the computer cold? Because it left its Windows open."
    ]
    speak(random.choice(jokes))



def open_calculator():
    speak("Opening calculator.")
    subprocess.Popen("calc.exe")



def open_notepad():
    speak("Opening Notepad.")
    subprocess.Popen("notepad.exe")



def introduce_self():
    speak(f"I am {ASSISTANT_NAME}, your P.A.")



def list_capabilities():
    speak("I can tell the time and date, search Google or Youtube, open websites, check the weather, tell jokes and open some computer apps!")



def go_to_sleep():
    speak("Understood. Going dormant.")
    raise SystemExit

# --------------------------------
# COMMAND ROUTER
# --------------------------------
def handle_command(command):
    if not command:
        speak("I didn't catch that.")
        return

    if "time" in command:
        tell_time()

    elif "date" in command:
        tell_date()

    elif "open google" in command:
        open_google()

    elif "open youtube" in command:
        open_youtube()

    elif "open gmail" in command:
        open_gmail()

    elif "open github" in command:
        open_github()

    elif "open spotify" in command:
        open_spotify()

    elif "search youtube for" in command:
        search_term = command.replace("search youtube for", "").strip()
        search_youtube(search_term)

    elif "search for" in command:
        search_term = command.replace("search for", "").strip()
        search_google(search_term)

    elif "weather" in command:
        get_weather()

    elif "joke" in command:
        tell_joke()

    elif "open calculator" in command:
        open_calculator()

    elif "open notepad" in command:
        open_notepad()

    elif "how are you" in command:
        speak("I'm functioning perfectly!")

    elif "your name" in command:
        introduce_self()

    elif "what can you do" in command or "help" in command:
        list_capabilities()

    elif "stop" in command or "exit" in command or "sleep" in command:
        go_to_sleep()

    else:
        speak(f"You said: {command}")

# --------------------------------
# MAIN LOOP
# --------------------------------
def main():
    speak(f"Hello. {ASSISTANT_NAME} is now online.")

    while True:
        phrase = listen(DEFAULT_LISTEN_DURATION)

        if phrase:
            print(f"Detected phrase: {phrase}")

        if contains_wake_word(phrase):
            command = extract_command_from_phrase(phrase)

            if command:
                handle_command(command)
            else:
                speak("Yes?")
                follow_up_command = listen(COMMAND_LISTEN_DURATION)
                handle_command(follow_up_command)

        time.sleep(0.5)


# --------------------------------
# PROGRAM ENTRY POINT
# --------------------------------
if __name__ == "__main__":
    main()