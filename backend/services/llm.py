# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from typing import Generator

# load_dotenv(dotenv_path=".env", override=True)

# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])



# def ask(system_prompt: str) -> str:
#     response = client.responses.create(
#         model="gpt-4.1-mini",
#         input=system_prompt,
#         max_output_tokens=500,
#         temperature=0.3,
#     )
#     return response.output_text


# def ask_dev(system_prompt: str) -> str:
#     response = client.responses.create(
#         model="gpt-4.1-mini",
#         input=system_prompt,
#         max_output_tokens=600,
#         temperature=0.1,
#     )
#     return response.output_text


# def ask_stream(prompt: str):
#     def generator():
#         with client.responses.stream(
#             model="gpt-4.1-mini",
#             input=prompt,
#         ) as stream:
#             for event in stream:
#                 if event.type == "response.output_text.delta":
#                     yield event.delta

#     return generator()


import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Generator

load_dotenv(dotenv_path=".env", override=True)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def ask(system: str, user: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0.2,
        max_output_tokens=700,
    )
    return response.output_text


def ask_stream(system: str, user: str):
    def generator():
        try:
            with client.responses.stream(
                model="gpt-4.1-mini",
                input=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            ) as stream:
                for event in stream:
                    if event.type == "response.output_text.delta":
                        if isinstance(event.delta, str):
                            yield event.delta
        except Exception as e:
            print("❌ LLM STREAM ERROR:", repr(e))
            return

    return generator()
