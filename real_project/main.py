import sys
from assistant import NovaAssistant

sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    assistant = NovaAssistant()
    assistant.run()