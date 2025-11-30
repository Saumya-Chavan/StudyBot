# ...existing code...
"""Improved flashcard generator agent."""

def generate_flashcards(keywords, text, lang="en"):
    """
    Returns a list of flashcard dicts:
    [{"term":..., "meaning":..., "example":..., "difficulty":...}, ...]
    """
    flashcards = []
    if not keywords:
        return flashcards

    sentences = [s.strip() for s in str(text).split('.') if s.strip()]

    for key in keywords:
        example = ""
        key_str = str(key)
        key_lower = key_str.lower()
        for s in sentences:
            if key_lower in s.lower():
                example = s.strip()
                break

        flashcards.append({
            "term": key_str,
            "meaning": f"Important concept related to {key_str}. Review this concept.",
            "example": example or f"No example sentence found for {key_str}.",
            "difficulty": "medium"
        })

    return flashcards
# ...existing code...