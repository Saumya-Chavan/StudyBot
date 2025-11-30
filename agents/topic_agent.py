# agents/topic_agent.py
"""Classify the topic using keyword-based scoring."""

TOPIC_KEYWORDS = {
    "Operating Systems": ["process", "memory", "fragmentation", "cpu", "deadlock"],
    "DBMS": ["sql", "transaction", "schema", "table", "query"],
    "Computer Networks": ["protocol", "ip", "tcp", "udp", "router"],
    "OOP": ["class", "object", "inheritance", "polymorphism"],
    "DSA": ["tree", "graph", "stack", "queue", "algorithm"],
    "Maths": ["equation", "integral", "derivative", "matrix"],
}

def classify_topic(text):
    scores = {topic: 0 for topic in TOPIC_KEYWORDS}

    text_lower = text.lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        for w in keywords:
            if w in text_lower:
                scores[topic] += 1

    best_topic = max(scores, key=scores.get)
    return best_topic, scores
