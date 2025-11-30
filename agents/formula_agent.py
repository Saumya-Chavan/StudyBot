# agents/formula_agent.py
"""Extract mathematical formulas using regex."""

import re

FORMULA_REGEX = r"[A-Za-z]+\s*=\s*[^ \n]+"

def extract_formulas(text):
    formulas = re.findall(FORMULA_REGEX, text)
    return list(set(formulas))  # unique
