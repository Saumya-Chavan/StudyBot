import heapq
import re

class SummaryAgent:
    def process(self, text):
        """Generates an extractive summary based on word frequency."""
        # 1. Clean and tokenize
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        formatted_text = re.sub('[^a-zA-Z]', ' ', text)
        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        
        sentence_list = text.split('.')
        stopwords = set(["the", "and", "of", "to", "in", "is", "it", "that", "for"])

        # 2. Calculate word frequencies
        word_frequencies = {}
        for word in formatted_text.lower().split():
            if word not in stopwords:
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        if not word_frequencies: return "Text too short to summarize."

        max_frequency = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/max_frequency)

        # 3. Score sentences
        sentence_scores = {}
        for sent in sentence_list:
            for word in sent.lower().split():
                if word in word_frequencies:
                    if len(sent.split(' ')) < 30: # Limit long sentences
                        if sent not in sentence_scores:
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

      
        summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        return summary
