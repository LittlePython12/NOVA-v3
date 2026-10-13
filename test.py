import asyncio
import edge_tts
from playsound import playsound
import os

async def test():
    text = "Testing voice output."
    voice = "Microsoft Server Speech Text to Speech Voice (en-GB, RyanNeural)"
    file = "test.mp3"

    if os.path.exists(file):
        os.remove(file)

    communicate = edge_tts.Communicate(
        text = text,
        voice = voice,
        rate = "+0%",
        volume = "+0%",
        pitch = "+0%",
        boundary = "Sentence"
    )

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            with open(file, "ab") as f:
                f.write(chunk["data"])

    playsound(file)

asyncio.run(test())