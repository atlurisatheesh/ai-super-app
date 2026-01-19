# def intent(text: str) -> str:
#     t = text.lower()
#     if any(k in t for k in ["error","exception","stacktrace","bug"]): return "dev"
#     if any(k in t for k in ["interview","answer this","live"]): return "live"
#     if any(k in t for k in ["write","generate","copy","script"]): return "creative"
#     return "chat"


def intent(text: str) -> str:
    t = text.lower()

    # strict dev requests
    if any(k in t for k in [
        "ready to paste",
        "final code",
        "full script",
        "terraform script",
        "complete code",
        "production ready"
    ]):
        return "dev_strict"

    # debugging / errors
    if any(k in t for k in [
        "error", "exception", "stacktrace", "bug", "issue", "fails"
    ]):
        return "dev_explain"

    if any(k in t for k in ["interview", "answer this", "live"]):
        return "live"

    if any(k in t for k in ["write", "generate", "copy", "script"]):
        return "creative"

    return "chat"
