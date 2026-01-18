from app.services.llm import ask, ask_stream
from app.prompts import chat, dev, creative, live

def run(mode: str, text: str) -> str:
    if mode == "dev":
        return ask(dev.prompt(text))
    if mode == "creative":
        return ask(creative.prompt(text))
    if mode == "live":
        return ask(live.prompt(text))
    return ask(chat.prompt(text))


def run_stream(mode: str, text: str):
    if mode == "dev":
        return ask_stream(dev.prompt(text))
    if mode == "creative":
        return ask_stream(creative.prompt(text))
    if mode == "live":
        return ask_stream(live.prompt(text))
    return ask_stream(chat.prompt(text))
