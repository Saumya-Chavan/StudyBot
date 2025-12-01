from collections import Counter
import re

class ConceptAgent:
    def process(self, text):
        """Extracts top keywords and simulates weak point detection."""
        words = re.findall(r'\w+', text.lower())
        stopwords = set(["the", "and", "is", "of", "to", "in", "it", "that", "this", "for", "with", "as"])
        filtered = [w for w in words if w not in stopwords and len(w) > 4]
        
        common = Counter(filtered).most_common(10)
        keywords = [item[0] for item in common]
        
        
        weak_points = [w for w in keywords if len(w) > 7] 
        
        return {"keywords": keywords, "weak_points": weak_points}
