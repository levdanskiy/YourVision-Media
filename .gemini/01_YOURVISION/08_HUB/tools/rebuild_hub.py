import sys
import os

# Delegate to rebuild_perfect.py to avoid keeping duplicate templates
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rebuild_perfect import rebuild

if __name__ == "__main__":
    rebuild()
