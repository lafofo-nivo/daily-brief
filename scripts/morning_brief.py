#!/usr/bin/env python3
"""
Morning Brief - Unified daily report
Combines: Weather, Market, Calendar, Tasks
"""

import subprocess
import json
from datetime import datetime
import urllib.request
import os

def get_weather():
    """Get weather for Tel Aviv (Celsius)"""
    try:
        url = "https://wttr.in/Tel+Aviv?m&format=%c+%t+%h+%w"
        with urllib.request.urlopen(url, timeout=10) as r:
            weather = r.read().decode('utf-8').strip()
        return f"🌤️ **תל אביב:** {weather}"
    except:
        return "🌤️ מזג אוויר: לא זמין"

def get_market_summary():
    """Quick market snapshot"""
    try:
        # Use Yahoo Finance API for quick data
        symbols = {
            'BTC-USD': '₿ BTC',
            'SOL-USD': '◎ SOL', 
            '^GSPC': '📈 S&P500',
            'NVDA': '🟢 NVDA'
        }
        results = []
        for sym, label in symbols.items():
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = json.loads(r.read())
                    price = data['chart']['result'][0]['meta']['regularMarketPrice']
                    prev = data['chart']['result'][0]['meta']['previousClose']
                    change = ((price - prev) / prev) * 100
                    emoji = "🟢" if change >= 0 else "🔴"
                    results.append(f"{label}: ${price:,.2f} {emoji} {change:+.1f}%")
            except:
                pass
        return "\n".join(results) if results else "שווקים: לא זמין"
    except:
        return "שווקים: לא זמין"

def get_date_info():
    """Get formatted date in Hebrew (Israel time)"""
    import subprocess
    try:
        # Get Israel time
        result = subprocess.run(['date', '+%Y-%m-%d %H:%M', '-d', 'TZ="Asia/Jerusalem"'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            il_time = result.stdout.strip()
        else:
            # Fallback: UTC+2/+3
            from datetime import timedelta
            il_now = datetime.utcnow() + timedelta(hours=2)
            il_time = il_now.strftime('%Y-%m-%d %H:%M')
    except:
        from datetime import timedelta
        il_now = datetime.utcnow() + timedelta(hours=2)
        il_time = il_now.strftime('%Y-%m-%d %H:%M')
    
    now = datetime.strptime(il_time.split()[0], '%Y-%m-%d')
    days_he = ['שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת', 'ראשון']
    day_name = days_he[now.weekday()]
    time_str = il_time.split()[1] if len(il_time.split()) > 1 else ""
    return f"📅 **יום {day_name}, {now.strftime('%d/%m/%Y')}** | 🕐 {time_str} IL"

def get_tasks():
    """Get today's focus from HEARTBEAT.md"""
    try:
        heartbeat_path = os.path.expanduser("~/.openclaw/workspace/HEARTBEAT.md")
        if os.path.exists(heartbeat_path):
            with open(heartbeat_path, 'r') as f:
                content = f.read()
                # Extract first few meaningful lines
                lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
                if lines:
                    return "📋 **פוקוס היום:**\n" + "\n".join(lines[:5])
        return ""
    except:
        return ""

def build_brief():
    """Build the complete morning brief"""
    sections = []
    
    # Header
    sections.append("☀️ **בוקר טוב!**")
    sections.append("")
    
    # Date
    sections.append(get_date_info())
    sections.append("")
    
    # Weather
    sections.append(get_weather())
    sections.append("")
    
    # Markets
    sections.append("📊 **שווקים:**")
    sections.append(get_market_summary())
    sections.append("")
    
    # Tasks
    tasks = get_tasks()
    if tasks:
        sections.append(tasks)
        sections.append("")
    
    # Footer
    sections.append("---")
    sections.append("יום פרודוקטיבי! 🚀")
    
    return "\n".join(sections)

if __name__ == "__main__":
    brief = build_brief()
    print(brief)
