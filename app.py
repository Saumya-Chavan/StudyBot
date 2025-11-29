# app.py
"""
Offline StudyBot — Streamlit app (no OpenAI)
- 100% local offline heuristics
- Multi-agent: summary (sequential), question+concept (parallel)
- Saves outputs and persists simple memory.json
"""

import streamlit as st
from pathlib import Path
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

# -------------------------
# Utilities (tools)
# -------------------------
def text_stats(text: str):
    words = len(text.split())
    sentences = [s for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]
    return {"words": words, "sentences": len(sentences), "reading_time_min": round(words / 200, 2)}

def simple_summary_local(text: str, max_sentences: int = 3) -> str:
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]
    if not sents:
        return ""
    scored = sorted(sents, key=lambda s: len(s), reverse=True)
    chosen = scored[:max_sentences]
    chosen_sorted = [s for s in sents if s in chosen]
    return " ".join(chosen_sorted)

def extract_keywords_local(text: str, top_k: int = 6):
    STOP = set([
        "the","is","in","and","to","of","a","an","on","for","with","that","this","it","as","are",
        "by","be","or","from","at","which","was","were","has","have","but","not","they","their",
    ])
    tokens = re.findall(r"[A-Za-z']+", text.lower())
    tokens = [t for t in tokens if t not in STOP and len(t) > 3]
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(top_k)]

# -------------------------
# Agents (offline heuristics)
# -------------------------
def summary_agent(text: str) -> str:
    return simple_summary_local(text, max_sentences=4)

def question_generator_agent(summary: str) -> dict:
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
            mcqs.append({"q": s, "options": ["A", "B", "C", "D"], "answer": "A"})
    for s in sents[:4]:
        short.append("Explain: " + (s if len(s.split()) < 20 else " ".join(s.split()[:8]) + "..."))
    return {"mcqs": mcqs, "short": short}

def concept_checker_agent(text: str) -> dict:
    keywords = extract_keywords_local(text, top_k=8)
    flashcards = {k: f"Quick note: review the concept of {k}." for k in keywords}
    weak_points = []
    for s in re.split(r'(?<=[.!?])\s+', text):
        s_l = s.lower()
        if any(w in s_l for w in ["difficult", "confusing", "however", "but"]) and len(weak_points) < 4:
            weak_points.append(s.strip()[:120])
    if not weak_points:
        weak_points = keywords[-2:] if len(keywords) >= 2 else []
    return {"keywords": keywords, "flashcards": flashcards, "weak_points": weak_points}

# -------------------------
# Memory (simple JSON)
# -------------------------
MEM_FILE = Path("memory.json")

def load_memory():
    if MEM_FILE.exists():
        try:
            return json.loads(MEM_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"recent": [], "weak": [], "usage": 0}

def save_memory(topic, weak_points):
    mem = load_memory()
    recent = mem.get("recent", [])
    if topic:
        if topic in recent:
            recent.remove(topic)
        recent.insert(0, topic)
    mem["recent"] = recent[:5]
    wp = mem.get("weak", [])
    for w in weak_points:
        if w not in wp:
            wp.insert(0, w)
    mem["weak"] = wp[:8]
    mem["usage"] = mem.get("usage", 0) + 1
    MEM_FILE.write_text(json.dumps(mem, indent=2), encoding="utf-8")
    return mem

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="StudyBot (Offline)", layout="wide")
st.title("StudyBot — Offline Multi-Agent Study Helper")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input notes")
    uploaded = st.file_uploader(
        "Upload a notes.txt file or paste text below",
        type=["txt"]
    )
    paste = st.text_area("Or paste notes here (overrides upload)", height=250)
    run_btn = st.button("Analyze (offline)")

with col2:
    st.subheader("Memory & Info")
    mem = load_memory()
    st.write("Recent topics:", mem.get("recent", []))
    st.write("Weak points:", mem.get("weak", []))
    st.write("Usage count:", mem.get("usage", 0))
    st.markdown("---")
    st.write("This offline app uses simple rules — no internet or API needed.")

if run_btn:
    text = ""
    if paste and paste.strip():
        text = paste.strip()
    elif uploaded is not None:
        try:
            text = uploaded.getvalue().decode("utf-8")
        except:
            text = str(uploaded.getvalue())
    else:
        st.warning("Please upload notes or paste text.")
        st.stop()

    # Stats + Summary
    with st.spinner("Computing summary..."):
        stats = text_stats(text)
        st.metric("Words", stats["words"])
        st.metric("Sentences", stats["sentences"])
        st.write(f"Reading time (min): {stats['reading_time_min']}")
        summary = summary_agent(text)
        st.subheader("Summary")
        st.write(summary)

    # Run 2 agents in parallel
    st.subheader("Generating Questions & Concepts (parallel)")
    with st.spinner("Running agents..."):
        with ThreadPoolExecutor(max_workers=2) as ex:
            q_future = ex.submit(question_generator_agent, summary)
            c_future = ex.submit(concept_checker_agent, text)
            q_out = q_future.result()
            c_out = c_future.result()

    # Questions
    st.subheader("MCQs")
    for i, mcq in enumerate(q_out.get("mcqs", []), start=1):
        st.markdown(f"**Q{i}.** {mcq['q']}")
        for j, opt in enumerate(mcq["options"]):
            st.write(f"{chr(65+j)}. {opt}")
        st.write(f"**Answer:** {mcq['answer']}")
        st.write("")

    st.subheader("Short Answer Questions")
    for i, q in enumerate(q_out.get("short", []), start=1):
        st.write(f"{i}. {q}")

    # Concepts
    st.subheader("Keywords & Flashcards")
    st.write("Keywords:", ", ".join(c_out["keywords"]))
    for k, v in list(c_out["flashcards"].items())[:6]:
        st.write(f"- **{k}**: {v}")

    st.write("Weak points:", c_out["weak_points"])

    # Update memory
    topic = c_out["keywords"][0] if c_out["keywords"] else None
    updated_mem = save_memory(topic, c_out["weak_points"])
    st.success("Memory updated.")
    st.write(updated_mem)

    # Save session output
    outdir = Path("outputs")
    outdir.mkdir(exist_ok=True)
    ts = int(time.time())
    session_dir = outdir / f"session_{ts}"
    session_dir.mkdir()

    (session_dir / "input.txt").write_text(text)
    (session_dir / "summary.txt").write_text(summary)
    (session_dir / "questions.json").write_text(json.dumps(q_out, indent=2))
    (session_dir / "concepts.json").write_text(json.dumps(c_out, indent=2))

    st.info(f"Saved outputs to: {session_dir}")

st.markdown("---")
st.caption("Offline StudyBot — Multi-Agent System Demo")
