class TopicAgent:
    def process(self, text):
        """Classifies topic based on simple keyword matching."""
        text_lower = text.lower()
        topics = {
            "Computer Science": ["algorithm", "data", "memory", "cpu", "network", "database", "sql", "python"],
            "Physics": ["force", "motion", "energy", "velocity", "gravity", "newton"],
            "History": ["war", "empire", "king", "ancient", "century"],
            "Biology": ["cell", "plant", "animal", "dna", "species"]
        }
        
        scores = {topic: 0 for topic in topics}
        
        for topic, keywords in topics.items():
            for k in keywords:
                if k in text_lower:
                    scores[topic] += 1
                    
      
        best_topic = max(scores, key=scores.get)
        return best_topic if scores[best_topic] > 0 else "General Knowledge"
