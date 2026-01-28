#!/usr/bin/env python3
"""
ለፕሮጀክት ማስኬድ ማብራሪያ
"""

import subprocess
import sys
import os

def run_system():
    """ስርዓቱን ያስኬዳል"""
    
    # ጥገኝነቶችን ያረጋግጡ
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    # ስክሪፕት ካለ ያስኬዱ
    if os.path.exists("main.py"):
        print("🚀 Starting Profit Master System...")
        
        # ከ command line arguments ነጋሪቶችን ያግኙ
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--topic', default='AI Revolution')
        parser.add_argument('--language', default='am')
        args = parser.parse_args()
        
        # ስርዓቱን ያስኬዱ
        from main import main
        main()
        return True
    else:
        print("❌ main.py not found")
        return False

if __name__ == "__main__":
    run_system()
