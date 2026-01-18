BLOCK = ["hack","crack","bypass","cheat","pirate","steal"]
def legal(text: str) -> bool:
    t = text.lower()
    return not any(k in t for k in BLOCK)
