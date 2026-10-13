def contains_wake_word(phrase, wake_words):
    return any(wake_word in phrase for wake_word in wake_words)


def extract_command_from_phrase(phrase, wake_words):
    for wake_word in wake_words:
        if wake_word in phrase:
            return phrase.replace(wake_word, "").strip()
    return ""


def clean_weather_text(text):
    cleaned = text.strip()
    cleaned = cleaned.replace("°C", " degrees Celsius")
    cleaned = cleaned.replace("+", "plus ")
    cleaned = cleaned.replace("-", "minus ")
    return cleaned