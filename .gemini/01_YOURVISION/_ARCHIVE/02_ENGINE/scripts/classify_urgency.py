#!/usr/bin/env python3
import sys
import re

def classify(text):
    text = text.upper()
    # Маркеры абсолютной срочности
    breaking_markers = ["WINNER", "ПЕРЕМОЖЕЦЬ", "ПОБЕДИТЕЛЬ", "BREAKING", "DISQUALIFIED", "OFFICIAL STATEMENT", "МОЛНИЯ", "🚨"]
    # Маркеры высокой важности
    flash_markers = ["PREMIERE", "RELEASE", "REVEALED", "ПРЕМЬЕРА", "РЕЛИЗ", "ПРЕДСТАВЛЕНО", "⚡"]
    
    for m in breaking_markers:
        if m in text: return "BREAKING"
    
    for m in flash_markers:
        if m in text: return "FLASH"
        
    return "INFO"

if __name__ == "__main__":
    context = sys.stdin.read()
    print(classify(context))
