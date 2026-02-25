#!/usr/bin/env python3
"""
Publish updates to daily-brief GitHub repo
Usage: python3 publish_daily_brief.py <type> <title> <content>
"""
import json, sys, subprocess
from datetime import datetime, timedelta

REPO_DIR = "/tmp/daily-brief"

def add_entry(entry_type, title, content, source="Nivo"):
    """Add entry to summaries.json"""
    # Israel time (UTC+2)
    il_now = datetime.utcnow() + timedelta(hours=2)
    date_str = il_now.strftime("%Y-%m-%d")
    
    entry = {
        "date": date_str,
        "type": entry_type,
        "title": title,
        "content": content,
        "source": source,
        "ts": datetime.utcnow().isoformat() + "Z"
    }
    
    # Load existing
    with open(f"{REPO_DIR}/summaries.json", "r") as f:
        summaries = json.load(f)
    
    # Add to beginning
    summaries.insert(0, entry)
    
    # Save
    with open(f"{REPO_DIR}/summaries.json", "w") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Added {entry_type}: {title}")
    return entry

def git_push(message):
    """Commit and push changes"""
    subprocess.run(["git", "-C", REPO_DIR, "add", "summaries.json"], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", message], check=False)
    subprocess.run(["git", "-C", REPO_DIR, "push", "origin", "main"], check=True)
    print(f"✅ Pushed to GitHub")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: publish_daily_brief.py <type> <title> <content> [source]")
        sys.exit(1)
    
    entry_type = sys.argv[1]
    title = sys.argv[2]
    content = sys.argv[3]
    source = sys.argv[4] if len(sys.argv) > 4 else "Nivo"
    
    # Pull latest
    subprocess.run(["git", "-C", REPO_DIR, "pull"], check=True)
    
    # Add entry
    add_entry(entry_type, title, content, source)
    
    # Push
    git_push(f"Add {entry_type}: {title}")
