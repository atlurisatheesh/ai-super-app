# from services.llm import ask, ask_stream
# from prompts import chat, dev, creative, live

# def run(mode: str, text: str) -> str:
#     if mode == "dev":
#         return ask(dev.prompt(text))
#     if mode == "creative":
#         return ask(creative.prompt(text))
#     if mode == "live":
#         return ask(live.prompt(text))
#     return ask(chat.prompt(text))


# def run_stream(mode: str, text: str):
#     if mode == "dev":
#         return ask_stream(dev.prompt(text))
#     if mode == "creative":
#         return ask_stream(creative.prompt(text))
#     if mode == "live":
#         return ask_stream(live.prompt(text))
#     return ask_stream(chat.prompt(text))


from services.llm import ask, ask_stream
from prompts import chat, creative, live, dev

def run(mode: str, user_text: str) -> str:
    if mode in ("dev_explain", "dev_strict"):
        return ask(
            system=dev.system_prompt(mode),
            user=user_text
        )

    if mode == "creative":
        return ask(
            system=creative.prompt(user_text),
            user=user_text
        )

    if mode == "live":
        return ask(
            system=live.prompt(user_text),
            user=user_text
        )

    return ask(
        system=chat.prompt(user_text),
        user=user_text
    )


def run_stream(mode: str, user_text: str):
    if mode in ("dev_explain", "dev_strict"):
        return ask_stream(
            system=dev.system_prompt(mode),
            user=user_text
        )

    return ask_stream(
        system=chat.prompt(user_text),
        user=user_text
    )
