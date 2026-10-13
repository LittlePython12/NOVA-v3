from openai import OpenAI
import os

# Initialize the OpenAI client. It automatically looks for the OPENAI_API_KEY env variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def ask_gpt(prompt, conversation_history=None):
    if conversation_history is None:
        conversation_history = []

    # This is the system prompt that tells the AI its personality and role
    messages = [
        {
            "role": "system",
            "content": (
                "You are Nova, a helpful, intelligent voice assistant. "
                "Be concise, clear, and conversational. "
                "Keep your spoken responses natural and not overly long unless the user asks for detail."
            )
        }
    ]

    # Add the past conversation history
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )

        reply = response.choices[0].message.content
        print("RAW GPT REPLY:", reply)

        if reply is None:
            return "I received an empty response from the language model."

        return reply.strip()

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "I'm sorry, I had trouble reaching my language model."

