import webbrowser
import datetime
import requests
import urllib.parse
import random
import subprocess
from utils import clean_weather_text
from ai import ask_gpt


def tell_time(assistant):
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    assistant.speak(f"The time is {current_time}")


def tell_date(assistant):
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    assistant.speak(f"Today is {current_date}")


def open_google(assistant):
    assistant.speak("Opening Google.")
    webbrowser.open("https://www.google.com")


def open_youtube(assistant):
    assistant.speak("Opening YouTube.")
    webbrowser.open("https://www.youtube.com")


def open_gmail(assistant):
    assistant.speak("Opening Gmail.")
    webbrowser.open("https://mail.google.com")


def open_github(assistant):
    assistant.speak("Opening GitHub.")
    webbrowser.open("https://github.com")


def open_spotify(assistant):
    assistant.speak("Opening Spotify.")
    webbrowser.open("https://open.spotify.com")


def search_google(assistant, query):
    if not query:
        assistant.speak("What would you like me to search for?")
        return

    safe_query = urllib.parse.quote(query)
    assistant.speak(f"Searching Google for {query}.")
    webbrowser.open(f"https://www.google.com/search?q={safe_query}")


def search_youtube(assistant, query):
    if not query:
        assistant.speak("What would you like me to search for on YouTube?")
        return

    safe_query = urllib.parse.quote(query)
    assistant.speak(f"Searching YouTube for {query}.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={safe_query}")


def get_weather(assistant):
    assistant.speak("Checking the weather.")

    try:
        url = f"https://wttr.in/{assistant.city}?format=Temperature:+%t,+Condition:+%C"
        response = requests.get(url, timeout=5)

        weather_text = clean_weather_text(response.text)
        print(f"Weather response: {weather_text}")

        assistant.speak(f"The current weather in {assistant.city} is {weather_text}")

    except Exception as error:
        print(f"Weather Error: {error}")
        assistant.speak("I couldn't fetch the weather right now.")


def tell_joke(assistant):
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why did the developer go broke? Because he used up all his cache.",
        "I would tell you a UDP joke, but you might not get it.",
        "Why was the computer cold? Because it left its Windows open."
    ]
    assistant.speak(random.choice(jokes))


def open_calculator(assistant):
    assistant.speak("Opening calculator.")
    subprocess.Popen("calc.exe")


def open_notepad(assistant):
    assistant.speak("Opening notepad.")
    subprocess.Popen("notepad.exe")


def introduce_self(assistant):
    assistant.speak(f"I am {assistant.name}, your assistant.")


def list_capabilities(assistant):
    assistant.speak("I can tell the time and date, search Google or YouTube, open websites, check the weather, tell jokes, and open calculator or notepad.")


def go_to_sleep(assistant):
    assistant.speak("Understood. Going dormant.")
    raise SystemExit


def handle_command(assistant, command):
    if not command:
        assistant.speak("I didn’t catch that.")
        return

# ----------------------------------
#      NEW HANDLE COMMAND BLOCK
# ----------------------------------
def handle_command(assistant, command):
    if not command:
        assistant.speak("I didn't catch that.")
        return


    simple_commands = {
        "time": lambda: tell_time(assistant),
        "date": lambda: tell_time(assistant),
        "open google": lambda: open_google(assistant),
        "open youtube": lambda: open_youtube(assistant),
        "open gmail": lambda: open_gmail(assistant),
        "open github": lambda: open_github(assistant),
        "open spotify": lambda: open_spotify(assistant),
        "weather": lambda: get_weather(assistant),
        "joke": lambda: tell_joke(assistant),
        "open calculator": lambda: open_calculator(assistant),
        "open notepad": lambda: open_notepad(assistant),
        "how are you": lambda: assistant.speak("I'm functioning perfectly."),
        "your name": lambda: introduce_self(assistant),
        "what can you do": lambda: list_capabilities(assistant),
        "help": lambda: list_capabilities(assistant),
        "stop": lambda: go_to_sleep(assistant),
        "exit": lambda: go_to_sleep(assistant),
        "sleep": lambda: go_to_sleep(assistant),
    }

    # Check for simple, exact commands first
    for phrase, action in simple_commands.items():
        if phrase in command:
            action()
            return

    # Check for commands that require extracting a search term
    if "search youtube for" in command:
        search_term = command.replace("search youtube for", "").strip()
        search_youtube(assistant, search_term)
        return

    if "search for" in command:
        search_term = command.replace("search for", "").strip()
        search_google(assistant, search_term)
        return

    # --- THIS IS THE NEW PART: GPT FALLBACK ---
    # If no local command was matched, ask GPT
    print("No local command matched. Asking GPT...")
    gpt_reply = ask_gpt(command, assistant.conversation_history)

    if not gpt_reply:
        gpt_reply = "I'm sorry, I couldn't generate a response."

    # Update conversation history
    assistant.conversation_history.append({"role": "user", "content": command})
    assistant.conversation_history.append({"role": "assistant", "content": gpt_reply})

    # Speak the GPT response
    assistant.speak(str(gpt_reply))