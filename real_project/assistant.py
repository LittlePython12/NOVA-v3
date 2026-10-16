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
        self.input_mode = "voice" # For voice or text commands

    def speak(self, text):
        speak(text, self.voice, self.temp_audio_file, self.name)

    def listen(self, duration=None):
        if duration is None:
            duration = self.default_listen_duration
        return listen(duration, self.sample_rate)

    def toggle_mode(self):
        """Switch between voice and text input modes."""
        if self.input_mode == "voice":
            self.input_mode == "text"
            print("\n Switched to TEXT mode. Type your commands.")
            self.speak("Switched to text mode.")
        else:
            self.input_mode = "voice"
            print("\n Switched to VOICE mode. Speak to me.")
            self.speak("Switched to voice mode.")

    def run(self):
        self.speak(f"Hello. {self.name} is now online.")
        print("\nTip: Type 'switch mode' anytime to toggle between voice and text input.\n")

        while True:
            try:
                # --- TEXT MODE ---
                if self.input_mode == "text":
                    command = input("You (text): ").strip().lower()

                    if command in ["switch mode", "toggle mode", "voice mode"]:
                        self.toggle_mode()
                        continue

                    if command:
                        handle_command(self, command)

                # --- VOICE MODE ---
                else:
                    phrase = self.listen(self.default_listen_duration)

                    if phrase:
                        print(f"Detected phrase: {phrase}")

                    # Allow switching to text mode via voice
                    if "switch to text" in phrase or "text mode" in phrase:
                        self.toggle_mode()
                        continue

                    if contains_wake_word(phrase, self.wake_words):
                        command = extract_command_from_phrase(phrase, self.wake_words)

                        if command:
                            handle_command(self, command)
                        else:
                            self.speak("Yes?")
                            follow_up = self.listen(self.command_listen_duration)
                            handle_command(self, follow_up)

                    time.sleep(0.5)

            except KeyboardInterrupt:
                print("\Exiting Nova...")
                break