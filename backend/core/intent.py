def intent(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["error","exception","stacktrace","bug"]): return "dev"
    if any(k in t for k in ["interview","answer this","live"]): return "live"
    if any(k in t for k in ["write","generate","copy","script"]): return "creative"
    return "chat"
