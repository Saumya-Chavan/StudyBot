class FlashcardAgent:
    def process(self, keywords, text):
        """Creates Flashcards by finding definitions for keywords."""
        cards = []
        sentences = text.split('.')
        
        for word in keywords:
            for sent in sentences:
               
                if word in sent.lower() and ("is a" in sent or "refers to" in sent or "defined as" in sent):
                    cards.append({"term": word.capitalize(), "definition": sent.strip()})
                    break
        return cards
