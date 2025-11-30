# 📘 StudyBot — Offline Multi-Agent Study Assistant

**A Modular, Fully Offline AI System for Summaries, Questions, Flashcards & Insights.**

---

## 🔰 Overview

**StudyBot** is a fully offline, modular **multi-agent system** designed to help students transform raw study notes into structured learning material. Unlike standard wrappers around OpenAI or Gemini, StudyBot performs all logic locally using specialized agents.

**It supports:**
*  Summaries
*  MCQs & Short-answer questions
*  Keywords & Flashcards
*  Formula extraction
*  Topic classification & Weak-point detection
*  Dashboard analytics & Session memory

**All without using the internet, API keys, or cloud LLMs.**

> **Kaggle Context:** StudyBot is built for Kaggle’s **“Agentic AI Systems”** track and demonstrates real agent orchestration, tool usage, memory persistence, parallelism, and context engineering.

---

## 🧠 Features

### 🔹 Multi-Agent Architecture
StudyBot uses six independent agents to process information like a team of experts:

| Agent | Purpose | Execution Type |
| :--- | :--- | :--- |
| **Summary Agent** | Extracts key meaning from text | Sequential |
| **Question Agent** | Generates MCQs & SAQs | Parallel |
| **Concept Agent** | Identifies keywords & weak points | Parallel |
| **Flashcard Agent** | Creates detailed study cards | Specialized |
| **Formula Agent** | Detects mathematical formulas (Regex) | Specialized |
| **Topic Agent** | Predicts the subject matter | Specialized |

### 🔹 Agent Flow
1.  **Sequential:** `Summary Agent` runs first to grasp the global context.
2.  **Parallel:** `Question Agent` and `Concept Agent` run simultaneously using `ThreadPoolExecutor`.
3.  **Specialized:** `Flashcard`, `Formula`, and `Topic` agents refine the output based on extracted concepts.

### 🔹 Offline Tools
* **PDF Reader:** Uses `pdfplumber` for accurate text extraction.
* **Language Detector:** Script-based detection + `langdetect`.
* **Dashboard:** Interactive charts using `Plotly`.
* **Memory System:** Persistent JSON storage (`memory.json`) tracks usage, weak points, and study history.

---

## 📂 Project Structure

```text
StudyBot/
│
├── app.py                     # Main entry point (Streamlit UI + agent orchestration)
│
├── agents/                    # The Brains (Logic Layer)
│   ├── summary_agent.py
│   ├── question_agent.py
│   ├── concept_agent.py
│   ├── flashcard_agent.py
│   ├── formula_agent.py
│   └── topic_agent.py
│
├── utils/                     # The Tools (Helper Layer)
│   ├── pdf_reader.py
│   ├── language_utils.py
│   ├── file_utils.py
│   └── charts.py
│
├── memory.json                # Persistent local memory
├── README.md
├── requirements.txt
└── venv/
```
---

###  Example Input
- You can upload a PDF or paste raw text directly. Try pasting this example:

Normalization reduces redundancy. 1NF removes repeating groups. 2NF removes partial dependencies. 3NF removes transitive dependencies. Paging and segmentation manage memory efficiently.

** StudyBot will output: **

- A summary of Database Normalization.

- MCQs asking about specific Normal Forms.

- Flashcards defining 1NF, 2NF, etc.

- Classification as "Database Management Systems".

## Dashboard Features
- StudyBot includes an analytics dashboard to track long-term progress:

- **Topic Frequency:** What subjects have you studied most?

- **Weak Points:** Which concepts are you struggling with?

- **Usage Stats:** Total sessions and questions generated.

## Why This Project is Unique
- **100% Offline:** No dependency on OpenAI/Anthropic/Gemini APIs.

- **Real Orchestration:** Demonstrates how agents pass data (Context Engineering) rather than just chatting.

- **Parallel Processing:** Uses Python's ThreadPoolExecutor to run agents concurrently.

- **Observability:** Full visibility into the process via the Dashboard and logs.

#### This project satisfies Kaggle's Agentic AI requirements:

- Multi-Agent System

- Parallel & Sequential Execution

- Custom Tools

- Memory & State Management

- Deployment (Streamlit)

### Future Enhancements (Roadmap)
- Hybrid Mode: Optional toggle for GPT-4o / Gemini API when online.

- Audio Agent: Speech-to-Text for dictating notes.

- Export: Download flashcards as PDF/DOCX.

- Embeddings: Better topic classification via lightweight local embeddings.

- Spaced Repetition: Algorithm to schedule flashcard reviews.

## Author
Developed by Saumya Chavan For Kaggle: Agentic AI Systems – Project Submission
