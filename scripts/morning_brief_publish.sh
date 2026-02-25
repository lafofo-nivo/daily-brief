#!/bin/bash
# Morning Brief - Generate and publish to GitHub Pages

set -e

REPO_DIR="/tmp/daily-brief"
WORKSPACE="$HOME/.openclaw/workspace"

# Clone/update repo
cd /tmp
rm -rf daily-brief
git clone git@github.com:lafofo-nivo/daily-brief.git
cd daily-brief

# Generate brief and add to summaries.json
python3 << 'PYTHON'
import json
import subprocess
import urllib.request
from datetime import datetime, timedelta

# Get Israel time
il_now = datetime.utcnow() + timedelta(hours=2)
date_str = il_now.strftime("%Y-%m-%d")
time_str = il_now.strftime("%H:%M")
days_he = ['שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת', 'ראשון']
day_name = days_he[il_now.weekday()]

# Get weather
try:
    url = "https://wttr.in/Tel+Aviv?m&format=%c+%t+%h"
    with urllib.request.urlopen(url, timeout=10) as r:
        weather = r.read().decode('utf-8').strip()
except:
    weather = "לא זמין"

# Build content - simple and clean
content = f"""☀️ בוקר טוב!

📅 יום {day_name}, {il_now.strftime('%d/%m/%Y')} | 🕐 {time_str} IL

🌤️ תל אביב: {weather}

יום פרודוקטיבי! 🚀"""

# Read existing summaries
with open('summaries.json', 'r') as f:
    summaries = json.load(f)

# Create new entry
new_entry = {
    "date": date_str,
    "type": "morning",
    "title": f"Morning Brief - {il_now.strftime('%b %d')}",
    "content": content,
    "source": "Nivo",
    "ts": datetime.utcnow().isoformat() + "+00:00"
}

# Add to beginning
summaries.insert(0, new_entry)

# Save
with open('summaries.json', 'w') as f:
    json.dump(summaries, f, indent=2, ensure_ascii=False)

print(content)
print("\n---")
print("✅ Published to daily-brief")
PYTHON

# Commit and push
git add -A
git commit -m "Morning Brief - $(TZ=Asia/Jerusalem date '+%Y-%m-%d %H:%M')" || true
git push origin main

echo ""
echo "🔗 https://lafofo-nivo.github.io/daily-brief/"
