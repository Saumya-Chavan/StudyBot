# agents/summary_agent.py
"""Summary agent (offline heuristics)"""

import re
from collections import Counter

def simple_summary_local(text: str, max_sentences: int = 4) -> str:
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]
    if not sents:
        return ""
    scored = sorted(sents, key=lambda s: len(s), reverse=True)
    chosen = scored[:max_sentences]
    chosen_sorted = [s for s in sents if s in chosen]
    return " ".join(chosen_sorted)

def summarize_text(text: str, lang: str = "en") -> str:
    # For now, same heuristic for all languages; extended behavior can be added
    return simple_summary_local(text, max_sentences=4)
