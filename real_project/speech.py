import sounddevice as sd
import speech_recognition as sr
import asyncio
import edge_tts
import os
from playsound import playsound


async def speak_async(text, voice, temp_audio_file, assistant_name):
    print(f"{assistant_name}: {text}")

    try:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)

        communicate = edge_tts.Communicate(text, voice)

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                with open(temp_audio_file, "ab") as file:
                    file.write(chunk["data"])

        playsound(temp_audio_file)

    except Exception as error:
        print(f"TTS Error: {error}")

    finally:
        if os.path.exists(temp_audio_file):
            try:
                os.remove(temp_audio_file)
            except Exception:
                pass


def speak(text, voice, temp_audio_file, assistant_name):
    asyncio.run(speak_async(text, voice, temp_audio_file, assistant_name))


def listen(duration, sample_rate):
    recognizer = sr.Recognizer()
    print("🎙 Listening...")

    try:
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )
        sd.wait()

        audio_bytes = audio_data.tobytes()
        audio = sr.AudioData(audio_bytes, sample_rate, 2)

        query = recognizer.recognize_google(audio, language="en-US").lower()
        print(f"You said: {query}")
        return query

    except sr.UnknownValueError:
        print("No speech recognized.")
        return ""

    except sr.RequestError:
        print("Speech recognition service unavailable.")
        return ""

    except Exception as error:
        print(f"Listen Error: {error}")
        return ""