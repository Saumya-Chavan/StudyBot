import random
import re

class QuestionAgent:
    def process(self, text):
        """Generates simple Fill-in-the-Blank MCQs."""
        sentences = [s.strip() for s in text.split('.') if len(s) > 20]
        questions = []
        
        selected_sentences = random.sample(sentences, min(len(sentences), 5))
        
        for sent in selected_sentences:
            words = sent.split()
            # Pick a random word that is long enough (likely a keyword)
            candidates = [w for w in words if len(w) > 5]
            if not candidates: continue
            
            answer = random.choice(candidates)
            clean_answer = re.sub(r'[^\w]', '', answer) # Remove punctuation
            
            question_text = sent.replace(answer, "______")
            
            # Generate dummy distractors 
            distractors = ["None of the above", "Variable", "Process", "Algorithm"]
            options = [clean_answer] + distractors[:3]
            random.shuffle(options)
            
            questions.append({
                "question": question_text,
                "options": options,
                "answer": clean_answer
            })
            
        return questions
