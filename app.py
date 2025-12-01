import streamlit as st
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Import Utils
from utils.pdf_reader import extract_text_from_pdf
from utils.language_utils import detect_language
from utils.charts import plot_topic_frequency, plot_weak_points

# Import Agents
from agents.summary_agent import SummaryAgent
from agents.question_agent import QuestionAgent
from agents.concept_agent import ConceptAgent
from agents.formula_agent import FormulaAgent
from agents.flashcard_agent import FlashcardAgent
from agents.topic_agent import TopicAgent

# --- Configuration ---
MEMORY_FILE = "memory.json"
st.set_page_config(page_title="StudyBot Offline", layout="wide", page_icon="📘")

# --- Helper: Memory Management ---
def load_memory():
    default_memory = {"topics": {}, "weak_points": {}, "usage_count": 0}
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                # Merge loaded data with defaults to ensure all keys exist
                for key, value in default_memory.items():
                    if key not in data:
                        data[key] = value
                return data
        except json.JSONDecodeError:
            return default_memory
    return default_memory

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_memory(topic, weak_points):
    data = load_memory()
    # Update Topic Count
    data["topics"][topic] = data["topics"].get(topic, 0) + 1
    # Update Weak Points
    for wp in weak_points:
        data["weak_points"][wp] = data["weak_points"].get(wp, 0) + 1
    data["usage_count"] += 1
    save_memory(data)
    return data

# --- Main UI ---
st.title("📘 StudyBot —" \
" Offline Multi-Agent Assistant")
st.markdown("A **fully offline** AI system for summaries, flashcards, and testing.")

# Sidebar
with st.sidebar:
    st.header("📂 Input Data")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    raw_text = st.text_area("Or Paste Text Here", height=150)
    process_btn = st.button("🚀 Process Notes")
    
    st.divider()
    st.info("System Status: Ready (Offline Mode)")

# --- Agent Orchestration ---
if process_btn and (uploaded_file or raw_text):
    
    # 1. Text Extraction
    with st.spinner("Extracting text..."):
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                text_content = extract_text_from_pdf(uploaded_file)
            else:
                text_content = uploaded_file.read().decode("utf-8")
        else:
            text_content = raw_text
            
    if len(text_content) < 50:
        st.error("Text is too short to analyze. Please provide more content.")
    else:
        # 2. Language Detection & Topic (Fast Sequential)
        lang = detect_language(text_content)
        topic_agent = TopicAgent()
        detected_topic = topic_agent.process(text_content)
        
        st.success(f"Language: {lang} | Topic: {detected_topic}")
        
        # 3. Parallel Execution (Multi-Agent)
        with st.spinner("Agents are analyzing (Parallel Execution)..."):
            start_time = time.time()
            
            # Using ThreadPool to simulate multi-agent environment
            with ThreadPoolExecutor() as executor:
                future_summary = executor.submit(SummaryAgent().process, text_content)
                future_concept = executor.submit(ConceptAgent().process, text_content)
                future_questions = executor.submit(QuestionAgent().process, text_content)
                future_formulas = executor.submit(FormulaAgent().process, text_content)
            
            # Gather Results
            summary = future_summary.result()
            concepts = future_concept.result()
            questions = future_questions.result()
            formulas = future_formulas.result()
            
            # Dependent Agent (Needs concepts first)
            flashcards = FlashcardAgent().process(concepts['keywords'], text_content)
            
            # Update Memory
            memory_data = update_memory(detected_topic, concepts['weak_points'])
            
            exec_time = round(time.time() - start_time, 2)
            st.toast(f"Processing complete in {exec_time}s")

        # --- Display Results ---
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Summary", "❓ Quiz", "🗂️ Flashcards", "➗ Formulas", "📊 Dashboard"])
        
        with tab1:
            st.subheader("Key Takeaways")
            st.write(summary)
            
        with tab2:
            st.subheader("Practice Questions")
            for i, q in enumerate(questions):
                st.write(f"**Q{i+1}: {q['question']}**")
                user_ans = st.radio(f"Select answer for Q{i+1}", q['options'], key=f"q{i}")
                if st.button(f"Check Answer {i+1}", key=f"btn{i}"):
                    if user_ans == q['answer']:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. Answer: {q['answer']}")
                st.divider()

        with tab3:
            st.subheader("Concept Flashcards")
            if flashcards:
                col1, col2 = st.columns(2)
                for i, card in enumerate(flashcards):
                    with (col1 if i % 2 == 0 else col2):
                        with st.expander(f"📌 {card['term']}"):
                            st.write(f"**Definition:** {card['definition']}")
            else:
                st.info("No definitions found for generated keywords.")

        with tab4:
            st.subheader("Detected Formulas")
            if formulas:
                for f in formulas:
                    st.code(f, language="latex")
            else:
                st.info("No mathematical formulas detected.")

        with tab5:
            st.subheader("Learning Analytics")
            col_a, col_b = st.columns(2)
            with col_a:
                fig1 = plot_topic_frequency(memory_data)
                if fig1: st.plotly_chart(fig1, use_container_width=True)
            with col_b:
                fig2 = plot_weak_points(memory_data)
                if fig2: st.plotly_chart(fig2, use_container_width=True)
