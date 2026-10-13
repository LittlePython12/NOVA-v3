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


class NovaAssistant:
    def __init__(self):
        self.name = "Nova"
        self.wake_words = ["nova", "hey nova"]
        self.voice = "en-GB-RyanNeural"
        self.temp_audio_file = "temp_output.mp3"
        self.city = "Regina"
        self.sample_rate = 44100
        self.default_listen_duration = 5
        self.command_listen_duration = 6

    # --------------------------------
    # TEXT TO SPEECH
    # --------------------------------
    async def speak_async(self, text):
        print(f"{self.name}: {text}")

        try:
            if os.path.exists(self.temp_audio_file):
                os.remove(self.temp_audio_file)

            communicate = edge_tts.Communicate(text, self.voice)

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    with open(self.temp_audio_file, "ab") as file:
                        file.write(chunk["data"])

            playsound(self.temp_audio_file)

        except Exception as error:
            print(f"TTS Error: {error}")

        finally:
            if os.path.exists(self.temp_audio_file):
                try:
                    os.remove(self.temp_audio_file)
                except Exception:
                    pass

    def speak(self, text):
        asyncio.run(self.speak_async(text))

    # --------------------------------
    # SPEECH TO TEXT
    # --------------------------------
    def listen(self, duration=None):
        if duration is None:
            duration = self.default_listen_duration

        recognizer = sr.Recognizer()
        print("🎙 Listening...")

        try:
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16"
            )
            sd.wait()

            audio_bytes = audio_data.tobytes()
            audio = sr.AudioData(audio_bytes, self.sample_rate, 2)

            query = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"You said: {query}")
            return query

        except sr.UnknownValueError:
            print("No speech recognized.")
            return ""

        except sr.RequestError:
            print("Speech recognition service unavailable.")
            self.speak("Speech service is unavailable.")
            return ""

        except Exception as error:
            print(f"Listen Error: {error}")
            return ""

    # --------------------------------
    # HELPER FUNCTIONS
    # --------------------------------
    def contains_wake_word(self, phrase):
        return any(wake_word in phrase for wake_word in self.wake_words)

    def extract_command_from_phrase(self, phrase):
        for wake_word in self.wake_words:
            if wake_word in phrase:
                return phrase.replace(wake_word, "").strip()
        return ""

    def clean_weather_text(self, text):
        cleaned = text.strip()
        cleaned = cleaned.replace("°C", " degrees Celsius")
        cleaned = cleaned.replace("+", "plus ")
        cleaned = cleaned.replace("-", "minus ")
        return cleaned

    # --------------------------------
    # COMMAND ACTIONS
    # --------------------------------
    def tell_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {current_time}")

    def tell_date(self):
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {current_date}")

    def open_google(self):
        self.speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    def open_youtube(self):
        self.speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    def open_gmail(self):
        self.speak("Opening Gmail.")
        webbrowser.open("https://mail.google.com")

    def open_github(self):
        self.speak("Opening GitHub.")
        webbrowser.open("https://github.com")

    def open_spotify(self):
        self.speak("Opening Spotify.")
        webbrowser.open("https://open.spotify.com")

    def search_google(self, query):
        if not query:
            self.speak("What would you like me to search for?")
            return

        safe_query = urllib.parse.quote(query)
        self.speak(f"Searching Google for {query}.")
        webbrowser.open(f"https://www.google.com/search?q={safe_query}")

    def search_youtube(self, query):
        if not query:
            self.speak("What would you like me to search for on YouTube?")
            return

        safe_query = urllib.parse.quote(query)
        self.speak(f"Searching YouTube for {query}.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={safe_query}")

    def get_weather(self):
        self.speak("Checking the weather.")

        try:
            url = f"https://wttr.in/{self.city}?format=Temperature:+%t,+Condition:+%C"
            response = requests.get(url, timeout=5)

            weather_text = self.clean_weather_text(response.text)
            print(f"Weather response: {weather_text}")

            self.speak(f"The current weather in {self.city} is {weather_text}")

        except Exception as error:
            print(f"Weather Error: {error}")
            self.speak("I couldn't fetch the weather right now.")

    def tell_joke(self):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why did the developer go broke? Because he used up all his cache.",
            "I would tell you a UDP joke, but you might not get it.",
            "Why was the computer cold? Because it left its Windows open."
        ]
        self.speak(random.choice(jokes))

    def open_calculator(self):
        self.speak("Opening calculator.")
        subprocess.Popen("calc.exe")

    def open_notepad(self):
        self.speak("Opening notepad.")
        subprocess.Popen("notepad.exe")

    def introduce_self(self):
        self.speak(f"I am {self.name}, your assistant.")

    def list_capabilities(self):
        self.speak("I can tell the time and date, search Google or YouTube, open websites, check the weather, tell jokes, and open calculator or notepad.")

    def go_to_sleep(self):
        self.speak("Understood. Going dormant.")
        raise SystemExit

    # --------------------------------
    # COMMAND ROUTER
    # --------------------------------
    def handle_command(self, command):
        if not command:
            self.speak("I didn’t catch that.")
            return

        if "time" in command:
            self.tell_time()

        elif "date" in command:
            self.tell_date()

        elif "open google" in command:
            self.open_google()

        elif "open youtube" in command:
            self.open_youtube()

        elif "open gmail" in command:
            self.open_gmail()

        elif "open github" in command:
            self.open_github()

        elif "open spotify" in command:
            self.open_spotify()

        elif "search youtube for" in command:
            search_term = command.replace("search youtube for", "").strip()
            self.search_youtube(search_term)

        elif "search for" in command:
            search_term = command.replace("search for", "").strip()
            self.search_google(search_term)

        elif "weather" in command:
            self.get_weather()

        elif "joke" in command:
            self.tell_joke()

        elif "open calculator" in command:
            self.open_calculator()

        elif "open notepad" in command:
            self.open_notepad()

        elif "how are you" in command:
            self.speak("I'm functioning perfectly.")

        elif "your name" in command:
            self.introduce_self()

        elif "what can you do" in command or "help" in command:
            self.list_capabilities()

        elif "stop" in command or "exit" in command or "sleep" in command:
            self.go_to_sleep()

        else:
            self.speak(f"You said: {command}")

    # --------------------------------
    # MAIN LOOP
    # --------------------------------
    def run(self):
        self.speak(f"Hello. {self.name} is now online.")

        while True:
            phrase = self.listen(self.default_listen_duration)

            if phrase:
                print(f"Detected phrase: {phrase}")

            if self.contains_wake_word(phrase):
                command = self.extract_command_from_phrase(phrase)

                if command:
                    self.handle_command(command)
                else:
                    self.speak("Yes?")
                    follow_up_command = self.listen(self.command_listen_duration)
                    self.handle_command(follow_up_command)

            time.sleep(0.5)


if __name__ == "__main__":
    assistant = NovaAssistant()
    assistant.run()