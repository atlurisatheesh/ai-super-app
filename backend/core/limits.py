MAX_CHARS = 4000

def validate_size(text: str):
    if not text:
        raise ValueError("Message cannot be empty")

    if len(text) > MAX_CHARS:
        raise ValueError(
            f"Input too long ({len(text)} chars). Max allowed is {MAX_CHARS}."
        )
