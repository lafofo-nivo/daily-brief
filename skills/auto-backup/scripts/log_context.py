#!/usr/bin/env python3
"""
Log conversation context to daily markdown file.
Usage: python3 log_context.py "Summary or context to log"
"""

import sys
import os
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path.home() / ".openclaw" / "backup"
LOGS_DIR = BACKUP_DIR / "logs"

def ensure_dirs():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def get_today_log():
    return LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"

def log_entry(content: str):
    ensure_dirs()
    log_file = get_today_log()
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Create file with header if new
    if not log_file.exists():
        header = f"# Log - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        log_file.write_text(header)
    
    # Append entry
    entry = f"## [{timestamp}]\n\n{content}\n\n---\n\n"
    with open(log_file, "a") as f:
        f.write(entry)
    
    print(f"✅ Logged to {log_file}")
    return log_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 log_context.py \"Your context or summary\"")
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    log_entry(content)
