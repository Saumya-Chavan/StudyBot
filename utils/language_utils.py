
"""Simple language detection helpers (Devanagari vs English)."""

import re
try:
    from langdetect import detect
    LANGDETECT_AVAILABLE = True
except Exception:
    LANGDETECT_AVAILABLE = False

DEVANAGARI_RE = re.compile(r'[\u0900-\u097F]')

def is_devanagari(text: str) -> bool:
    return bool(DEVANAGARI_RE.search(text))

def detect_language(text: str) -> str:
    sample = text[:1000] if len(text) > 1000 else text
    if LANGDETECT_AVAILABLE:
        try:
            code = detect(sample)
            if code.startswith("hi") or is_devanagari(text):
                return "hi"
            elif code.startswith("mr"):
                return "mr"
            else:
                return "en"
        except Exception:
            pass
    if is_devanagari(sample):
        return "hi"
    return "en"
