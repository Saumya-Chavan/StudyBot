# app.py
"""
StudyBot (modular) — Offline Multi-Agent Study Helper (Level 2)
Entry point for the Streamlit UI. Uses modular agents and utils.
Includes:
 - summary, question, concept agents (Level 1)
 - flashcard, formula, topic agents (Level 2)
 - dashboard charts using utils/charts (Plotly)
 - PDF & language helpers from utils
"""

import streamlit as st
from pathlib import Path
import json
import time
from concurrent.futures import ThreadPoolExecutor

# Level 1 agents
from agents.summary_agent import summarize_text
from agents.question_agent import generate_questions
from agents.concept_agent import analyze_concepts

# Level 2 agents
from agents.flashcard_agent import generate_flashcards
from agents.formula_agent import extract_formulas
from agents.topic_agent import classify_topic

# utils
from utils.pdf_reader import extract_text_from_pdf_bytes
from utils.language_utils import detect_language
from utils.file_utils import (
    save_session_outputs,
    load_memory,
    save_memory,
)

# charts (Plotly) with safe fallback
try:
    from utils.charts import (
        plot_topic_frequency,
        plot_weakpoint_frequency,
        plot_usage_count,
    )
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False

st.set_page_config(page_title="StudyBot ", layout="wide")
st.sidebar.title("StudyBot")
st.sidebar.info("Offline modular StudyBot : PDF support, language detection, improved UI, dashboard & agents.")

page = st.sidebar.radio("Navigate", ["Home", "Analyze Notes", "Dashboard", "Memory", "About"])

# -------------------------
# HOME
# -------------------------
if page == "Home":
    st.title("StudyBot — Offline Multi-Agent Study Helper ")
    st.markdown(
        """
        Modular StudyBot converts notes to summaries, questions, keywords, flashcards, and insights.
        And adds dashboard charts, flashcard agent, formula extraction, and topic classification.
        """
    )
    st.write("Use **Analyze Notes** to upload `.txt` or `.pdf` or paste text. Dashboard shows aggregated stats.")

# -------------------------
# ANALYZE NOTES
# -------------------------
if page == "Analyze Notes":
    st.header("Analyze Notes")
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader("Upload notes (.txt or .pdf) or paste text", type=["txt", "pdf"])
        paste = st.text_area("Or paste notes here (paste overrides uploaded file)", height=260)
        user_topic = st.text_input("Optional: Topic label (e.g., 'Fragmentation in OS')")
    with col2:
        st.markdown("Settings")
        show_stats = st.checkbox("Show text stats", value=True)
        run_btn = st.button("Analyze (offline)")

    if run_btn:
        # get text content
        text = ""
        if paste and paste.strip():
            text = paste.strip()
        elif uploaded is not None:
            fname = uploaded.name.lower()
            if fname.endswith(".pdf"):
                text = extract_text_from_pdf_bytes(uploaded)
                if not text:
                    st.warning("PDF extraction returned no text. If the PDF is scanned (image), OCR is required.")
            else:
                try:
                    raw = uploaded.getvalue()
                    text = raw.decode("utf-8")
                except Exception:
                    text = str(uploaded.getvalue())
        else:
            st.warning("Please upload a file or paste text.")
            st.stop()

        if not text.strip():
            st.warning("No text to process.")
            st.stop()

        # language detection
        lang = detect_language(text)
        lang_name = "Devanagari (Hindi/Marathi)" if lang != "en" else "English"
        st.success(f"Detected language: {lang_name}")

        # summary (sequential)
        with st.spinner("Generating summary..."):
            summary = summarize_text(text, lang=lang)
            if show_stats:
                from utils.file_utils import text_stats
                stats = text_stats(text)
                st.metric("Words", stats["words"])
                st.metric("Sentences", stats["sentences"])
                st.write(f"Reading time (min): {stats['reading_time_min']}")

            st.subheader("Summary")
            st.write(summary)

        # run question + concept agents in parallel
        st.subheader("Questions & Concepts")
        with st.spinner("Running agents in parallel..."):
            with ThreadPoolExecutor(max_workers=2) as ex:
                qf = ex.submit(generate_questions, summary, lang)
                cf = ex.submit(analyze_concepts, text, lang)
                q_out = qf.result()
                c_out = cf.result()

        # display questions
        st.markdown("### Multiple Choice Questions (sample)")
        for i, mcq in enumerate(q_out.get("mcqs", []), start=1):
            st.markdown(f"**Q{i}.** {mcq.get('q')}")
            for j, opt in enumerate(mcq.get("options", [])):
                st.write(f"{chr(65+j)}. {opt}")
            st.write(f"**Answer:** {mcq.get('answer')}")
            st.write("")

        st.markdown("### Short-answer Questions")
        for i, q in enumerate(q_out.get("short", []), start=1):
            st.write(f"{i}. {q}")

        # concepts
        st.markdown("### Keywords & Flashcards (concept agent)")
        st.write(", ".join(c_out.get("keywords", [])))
        for k, v in list(c_out.get("flashcards", {}).items())[:8]:
            st.write(f"- **{k}**: {v}")
        st.write("Weak points:", c_out.get("weak_points", []))

        # -------------------------
        # Level 2 agents: flashcards, formulas, topic
        # -------------------------
        st.subheader("Flashcards (improved)")
        flashcards = generate_flashcards(c_out.get("keywords", []), text, lang)
        if flashcards:
            for card in flashcards[:8]:
                st.markdown(f"**{card['term']}** — {card['meaning']}")
                if card.get("example"):
                    st.write("Example:", card["example"])
                st.write("Difficulty:", card.get("difficulty", "medium"))
                st.write("---")
        else:
            st.write("No flashcards generated.")

        st.subheader("Extracted Formulas")
        formulas = extract_formulas(text)
        if formulas:
            for f in formulas:
                st.write("- " + f)
        else:
            st.write("No formulas detected.")

        st.subheader("Predicted Topic")
        topic, scores = classify_topic(text)
        st.success(f"Predicted Topic: **{topic}**")
        st.write("Topic scores:", scores)

        # save outputs + memory
        session_dir = save_session_outputs(text, summary, q_out, c_out, label=user_topic)
        topic_label = user_topic or (c_out.get("keywords",[None])[0] if c_out.get("keywords") else None)
        saved_mem = save_memory(topic_label, c_out.get("weak_points", []))
        st.success(f"Saved outputs to {session_dir}")
        st.write("Memory updated:", saved_mem)

# -------------------------
# DASHBOARD (Level 2 charts)
# -------------------------
if page == "Dashboard":
    st.header("Dashboard — Study Insights")
    mem = load_memory()

    st.subheader("Most Studied Topics")
    if PLOTLY_AVAILABLE:
        fig1 = plot_topic_frequency(mem.get("recent", []))
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.write("No topic data yet.")
    else:
        st.info("Plotly not installed — install plotly to see charts.")

    st.subheader("Weak Points Over Time")
    if PLOTLY_AVAILABLE:
        fig2 = plot_weakpoint_frequency(mem.get("weak", []))
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("No weak-point data yet.")
    else:
        st.info("Plotly not installed — install plotly to see charts.")

    st.subheader("Usage Count")
    if PLOTLY_AVAILABLE:
        fig3 = plot_usage_count(mem.get("usage", 0))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.write("Total sessions:", mem.get("usage", 0))

# -------------------------
# MEMORY
# -------------------------
if page == "Memory":
    st.header("Memory")
    mem = load_memory()
    st.write(mem)
    if st.button("Clear memory"):
        from utils.file_utils import clear_memory
        clear_memory()
        st.success("Memory cleared.")

# -------------------------
# ABOUT
# -------------------------
if page == "About":
    st.header("About StudyBot")
    st.markdown(
        """
        - StudyBot is an offline multi-agent study helper.
        -  1: PDF support, language detection, improved UI.
        -  2: Dashboard charts, flashcards, formula extraction, topic classification.
       
        """
    )
   

st.markdown("---")
st.caption("StudyBot — Offline Multi-Agent Study Helper ")
