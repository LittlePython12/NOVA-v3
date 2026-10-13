import time
from config import (
    ASSISTANT_NAME,
    WAKE_WORDS,
    VOICE,
    TEMP_AUDIO_FILE,
    CITY,
    SAMPLE_RATE,
    DEFAULT_LISTEN_DURATION,
    COMMAND_LISTEN_DURATION,
)
from speech import speak, listen
from utils import contains_wake_word, extract_command_from_phrase
from commands import handle_command


class NovaAssistant:
    def __init__(self):
        self.name = ASSISTANT_NAME
        self.wake_words = WAKE_WORDS
        self.voice = VOICE
        self.temp_audio_file = TEMP_AUDIO_FILE
        self.city = CITY
        self.sample_rate = SAMPLE_RATE
        self.default_listen_duration = DEFAULT_LISTEN_DURATION
        self.command_listen_duration = COMMAND_LISTEN_DURATION
        self.conversation_history = []

    def speak(self, text):
        speak(text, self.voice, self.temp_audio_file, self.name)

    def listen(self, duration=None):
        if duration is None:
            duration = self.default_listen_duration
        return listen(duration, self.sample_rate)

    def run(self):
        self.speak(f"Hello. {self.name} is now online.")

        while True:
            phrase = self.listen(self.default_listen_duration)

            if phrase:
                print(f"Detected phrase: {phrase}")

            if contains_wake_word(phrase, self.wake_words):
                command = extract_command_from_phrase(phrase, self.wake_words)

                if command:
                    handle_command(self, command)
                else:
                    self.speak("Yes?")
                    follow_up_command = self.listen(self.command_listen_duration)
                    handle_command(self, follow_up_command)

            time.sleep(0.5)