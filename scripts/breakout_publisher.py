#!/usr/bin/env python3
"""
Publish breakout stocks to daily-brief
Combines technical setups + catalysts + institutional activity
"""
import os, requests, re, json, subprocess
from datetime import datetime, timedelta

EXA_API_KEY = os.environ.get("EXA_API_KEY", "8fc77e5d-5509-43d1-983b-2be228275afb")
REPO_DIR = "/tmp/daily-brief"

def search(query, num=4, domains=None):
    """Search using Exa"""
    payload = {
        "query": query,
        "numResults": num,
        "type": "neural",
        "useAutoprompt": True,
        "contents": {"text": {"maxCharacters": 600}},
    }
    if domains:
        payload["includeDomains"] = domains
    
    try:
        resp = requests.post(
            "https://api.exa.ai/search",
            headers={"x-api-key": EXA_API_KEY, "Content-Type": "application/json"},
            json=payload,
            timeout=25,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
    except:
        return []

def find_breakouts():
    """Find specific breakout candidates"""
    
    # Search for specific stock mentions
    results = []
    
    # 1. Technical breakouts TODAY
    tech = search(
        "stocks breaking out today 2026 technical setup consolidation pattern high volume",
        num=3,
        domains=["investors.com", "finviz.com", "marketsmith.investors.com", "stockcharts.com"]
    )
    results.extend(tech)
    
    # 2. Unusual options activity (smart money)
    options = search(
        "unusual options activity today dark pool institutional buying smart money",
        num=3,
        domains=["benzinga.com", "unusual-whales.com", "marketbeat.com"]
    )
    results.extend(options)
    
    # 3. Analyst upgrades
    upgrades = search(
        "analyst upgrade price target raised today this week 2026",
        num=3,
        domains=["benzinga.com", "seekingalpha.com", "tipranks.com", "investors.com"]
    )
    results.extend(upgrades)
    
    return results

def extract_stocks(results):
    """Extract stock tickers and create summary"""
    # Common words to exclude
    exclude = {
        "NYSE", "NASDAQ", "SPY", "QQQ", "DIA", "IWM", "THE", "AND", "FOR", "BUY", 
        "SELL", "STOCK", "STOCKS", "ETF", "CEO", "CFO", "SEC", "IPO", "USA", "INC", 
        "LLC", "LTD", "CORP", "CO", "COMPANY", "TODAY", "THIS", "THAT", "WITH", "FROM",
        "ABOUT", "INTO", "HAVE", "HAS", "BEEN", "WERE", "WILL", "CAN", "ALL", "ALSO",
        "NEW", "NEWS", "AFTER", "BEFORE", "UP", "DOWN", "OUT", "OVER", "UNDER", "MORE",
        "MOST", "SOME", "WEEK", "MONTH", "YEAR", "DAY", "TIME", "MAY", "COULD", "WOULD",
        "SHOULD", "MUST", "WHICH", "THEIR", "THERE", "THESE", "THOSE", "VERY", "WELL",
        "STILL", "JUST", "NOW", "ONLY", "BACK", "THEN", "HERE", "WHERE", "WHEN", "WHY",
        "HOW", "WHO", "WHAT", "SAYS", "SAID", "GET", "GOT", "MAKE", "MADE", "TAKE", "TOOK"
    }
    
    mentions = {}
    
    for r in results:
        title = r.get("title", "")
        text = r.get("text", "")
        url = r.get("url", "")
        
        # Look for ticker patterns in title/text
        full_text = (title + " " + text).upper()
        
        # Pattern: $TICKER or (TICKER:
        tickers = re.findall(r'\$([A-Z]{1,5})\b', full_text)
        tickers += re.findall(r'\(([A-Z]{2,5}):', full_text)
        tickers += re.findall(r'\b([A-Z]{2,5})\)', full_text)
        
        for ticker in tickers:
            if ticker not in exclude and len(ticker) >= 2:
                if ticker not in mentions:
                    mentions[ticker] = {
                        "count": 0,
                        "title": title,
                        "snippet": text[:250].strip(),
                        "url": url
                    }
                mentions[ticker]["count"] += 1
    
    # Sort by mention count
    sorted_stocks = sorted(mentions.items(), key=lambda x: x[1]["count"], reverse=True)
    
    return sorted_stocks[:8]  # Top 8

def create_content(stocks):
    """Format content for daily brief"""
    if not stocks:
        return "No significant breakout setups detected today."
    
    content = "🚀 **Potential Breakout Stocks**\n\n"
    content += "Based on technical setups, unusual activity, and analyst upgrades:\n\n"
    
    for ticker, data in stocks[:5]:  # Top 5
        content += f"**${ticker}**\n"
        content += f"• {data['title'][:100]}...\n"
        if data['snippet']:
            content += f"• {data['snippet'][:150]}...\n"
        content += f"🔗 {data['url']}\n\n"
    
    content += "\n⚠️ Not financial advice - do your own research!"
    
    return content

def publish(content):
    """Publish to daily-brief"""
    subprocess.run(["git", "-C", REPO_DIR, "pull"], check=True)
    
    il_now = datetime.utcnow() + timedelta(hours=2)
    date_str = il_now.strftime("%Y-%m-%d")
    
    entry = {
        "date": date_str,
        "type": "market",
        "title": f"Breakout Watch - {il_now.strftime('%b %d')}",
        "content": content,
        "source": "Nivo Scan",
        "ts": datetime.utcnow().isoformat() + "Z"
    }
    
    with open(f"{REPO_DIR}/summaries.json", "r") as f:
        summaries = json.load(f)
    
    summaries.insert(0, entry)
    
    with open(f"{REPO_DIR}/summaries.json", "w") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)
    
    subprocess.run(["git", "-C", REPO_DIR, "add", "summaries.json"], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", f"Add breakout watch - {il_now.strftime('%b %d')}"], check=False)
    subprocess.run(["git", "-C", REPO_DIR, "push", "origin", "main"], check=True)
    
    print(f"✅ Published breakout watch to daily-brief")

def main():
    print("🔍 Scanning for breakout candidates...")
    results = find_breakouts()
    
    print("📊 Extracting stock mentions...")
    stocks = extract_stocks(results)
    
    print(f"✅ Found {len(stocks)} potential breakout stocks")
    
    content = create_content(stocks)
    print("\n" + content)
    
    print("\n📤 Publishing to daily-brief...")
    publish(content)

if __name__ == "__main__":
    main()
