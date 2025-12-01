import re

class FormulaAgent:
    def process(self, text):
        """Extracts potential mathematical formulas using Regex."""
       
        formula_pattern = r'[A-Za-z]+\s*=\s*[A-Za-z0-9\+\-\*\/\(\)\s]+'
        matches = re.findall(formula_pattern, text)
        
        # Filter out common false positives
        clean_formulas = [m.strip() for m in matches if len(m) > 5 and not m.lower().startswith("if")]
        return list(set(clean_formulas))
