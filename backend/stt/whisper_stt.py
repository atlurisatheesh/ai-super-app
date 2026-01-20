import whisper
import numpy as np

model = whisper.load_model("base")

def transcribe(chunks):
    audio = np.concatenate(chunks)
    result = model.transcribe(audio, fp16=False)
    return result["text"].strip()
