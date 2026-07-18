#!/usr/bin/env python3
import sys
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
target = os.path.join(script_dir, "..", "..", "..", "00_RULES", "stats-check.py")
os.execv(sys.executable, [sys.executable, target] + sys.argv[1:])
