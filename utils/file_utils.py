# utils/file_utils.py
"""Helpers for saving sessions and memory, plus small tools."""

from pathlib import Path
import json
import time
import re
from collections import Counter

OUT_DIR = Path("outputs")
MEM_FILE = Path("memory.json")

def text_stats(text: str):
    words = len(text.split())
    sentences = [s for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]
    return {"words": words, "sentences": len(sentences), "reading_time_min": round(words/200,2)}

def save_session_outputs(input_text, summary, questions, concepts, label=None):
    OUT_DIR.mkdir(exist_ok=True)
    ts = int(time.time())
    session_dir = OUT_DIR / f"session_{ts}"
    session_dir.mkdir()
    (session_dir / "input.txt").write_text(input_text, encoding="utf-8")
    (session_dir / "summary.txt").write_text(summary, encoding="utf-8")
    (session_dir / "questions.json").write_text(json.dumps(questions, indent=2), encoding="utf-8")
    (session_dir / "concepts.json").write_text(json.dumps(concepts, indent=2), encoding="utf-8")
    if label:
        (session_dir / "label.txt").write_text(str(label), encoding="utf-8")
    return session_dir

def load_memory():
    if MEM_FILE.exists():
        try:
            return json.loads(MEM_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"recent": [], "weak": [], "usage": 0}

def clear_memory():
    MEM_FILE.write_text(json.dumps({"recent": [], "weak": [], "usage": 0}, indent=2))

def save_memory(topic, weak_points):
    mem = load_memory()
    recent = mem.get("recent", [])
    if topic:
        if topic in recent:
            recent.remove(topic)
        recent.insert(0, topic)
    mem["recent"] = recent[:8]
    wp = mem.get("weak", [])
    for w in weak_points:
        if w not in wp:
            wp.insert(0,w)
    mem["weak"] = wp[:12]
    mem["usage"] = mem.get("usage", 0) + 1
    MEM_FILE.write_text(json.dumps(mem, indent=2), encoding="utf-8")
    return mem
