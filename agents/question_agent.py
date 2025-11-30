# agents/question_agent.py
"""Question generation agent (offline heuristics)"""

import re

def generate_questions(summary: str, lang: str = "en") -> dict:
    sents = [s for s in re.split(r'(?<=[.!?])\s+', summary) if s.strip()]
    mcqs = []
    short = []
    for s in sents[:4]:
        words = [w for w in re.findall(r"\w+", s) if len(w) > 4]
        if words:
            answer = words[0]
            q_text = s.replace(answer, "_____")
            options = [answer, answer + "X", "other", "none"]
            mcqs.append({"q": q_text, "options": options, "answer": answer})
        else:
            mcqs.append({"q": s, "options": ["A","B","C","D"], "answer":"A"})
    for s in sents[:4]:
        short.append("Explain: " + (s if len(s.split())<20 else " ".join(s.split()[:8]) + "..."))
    return {"mcqs": mcqs, "short": short}
