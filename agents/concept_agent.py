# agents/concept_agent.py
"""Concept checking agent: keywords, flashcards, weak points"""

import re
from collections import Counter
from utils.language_utils import is_devanagari

def extract_keywords_local(text: str, top_k: int = 8):
    STOP_ENG = set([
        "the","is","in","and","to","of","a","an","on","for","with","that","this","it","as","are",
        "by","be","or","from","at","which","was","were","has","have","but","not","they","their",
    ])
    if is_devanagari(text):
        tokens = re.findall(r"[\u0900-\u097F]+", text)
        tokens = [t for t in tokens if len(t) > 1]
        counts = Counter(tokens)
        return [w for w,_ in counts.most_common(top_k)]
    else:
        tokens = re.findall(r"[A-Za-z']+", text.lower())
        tokens = [t for t in tokens if t not in STOP_ENG and len(t) > 3]
        counts = Counter(tokens)
        return [w for w,_ in counts.most_common(top_k)]

def analyze_concepts(text: str, lang: str = "en") -> dict:
    keywords = extract_keywords_local(text, top_k=8)
    flashcards = {k: f"Quick note: review {k}." for k in keywords}
    weak_points = []
    for s in re.split(r'(?<=[.!?])\s+', text):
        s_l = s.lower()
        if any(w in s_l for w in ["difficult","confusing","however","but"]) and len(weak_points) < 4:
            weak_points.append(s.strip()[:120])
    if not weak_points:
        weak_points = keywords[-2:] if len(keywords) >= 2 else []
    return {"keywords": keywords, "flashcards": flashcards, "weak_points": weak_points}
