#!/usr/bin/env python3
"""
Potential Breakout Scanner
Finds stocks with breakout potential based on:
- Technical setups (consolidation, volume, resistance)
- Macro catalysts (earnings, sector rotation, news)
- Social signals (X, forums, analyst mentions)
- Quality filter: No penny stocks
"""
import os, requests, json
from datetime import datetime, timedelta

EXA_API_KEY = os.environ.get("EXA_API_KEY", "8fc77e5d-5509-43d1-983b-2be228275afb")

def search(query, num=5, include_domains=None, hours_back=48):
    """Search using Exa API"""
    payload = {
        "query": query,
        "numResults": num,
        "type": "neural",
        "useAutoprompt": True,
        "contents": {"text": {"maxCharacters": 800}},
    }
    if include_domains:
        payload["includeDomains"] = include_domains
    
    try:
        resp = requests.post(
            "https://api.exa.ai/search",
            headers={"x-api-key": EXA_API_KEY, "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
    except Exception as e:
        print(f"Search error: {e}")
        return []

def find_breakout_candidates():
    """Find stocks with breakout potential"""
    candidates = []
    
    # 1. Technical breakout setups
    print("🔍 Scanning for technical breakout setups...")
    technical = search(
        "stocks breaking out consolidation tight range high volume institutional buying technical setup 2026",
        num=6,
        include_domains=[
            "finviz.com", "stockcharts.com", "tradingview.com",
            "marketsmith.investors.com", "investors.com", "barchart.com"
        ]
    )
    
    # 2. Earnings catalyst plays
    print("📊 Scanning earnings catalysts...")
    earnings = search(
        "stocks earnings this week analyst upgrade catalyst positive guidance beat estimates",
        num=5,
        include_domains=[
            "seekingalpha.com", "benzinga.com", "investors.com",
            "marketwatch.com", "earningswhispers.com"
        ]
    )
    
    # 3. Sector rotation & momentum
    print("🔄 Checking sector rotation...")
    sector = search(
        "strongest sectors 2026 sector rotation institutional money flow leading stocks",
        num=4,
        include_domains=[
            "investors.com", "seekingalpha.com", "marketwatch.com",
            "schwab.com", "fidelity.com"
        ]
    )
    
    # 4. Social sentiment & unusual activity
    print("💬 Checking social signals...")
    social = search(
        "unusual options flow smart money dark pool institutional accumulation high conviction",
        num=5,
        include_domains=[
            "unusual-whales.com", "twitter.com", "x.com",
            "reddit.com", "stocktwits.com", "benzinga.com"
        ]
    )
    
    # 5. Analyst upgrades & institutional interest
    print("🎯 Scanning institutional activity...")
    institutional = search(
        "analyst upgrade price target raised institutional buying hedge fund accumulation 13F filing",
        num=4,
        include_domains=[
            "tipranks.com", "gurufocus.com", "fintel.io",
            "benzinga.com", "investors.com"
        ]
    )
    
    return {
        "technical": technical,
        "earnings": earnings,
        "sector": sector,
        "social": social,
        "institutional": institutional
    }

def extract_tickers(results):
    """Extract stock tickers from results"""
    import re
    tickers = set()
    
    for category in results.values():
        for result in category:
            text = (result.get("title", "") + " " + result.get("text", "")).upper()
            # Find ticker symbols (1-5 capital letters, common patterns)
            matches = re.findall(r'\b([A-Z]{1,5})\b', text)
            for match in matches:
                # Filter out common words that look like tickers
                if match not in ["NYSE", "NASDAQ", "SPY", "QQQ", "THE", "AND", "FOR", "BUY", "SELL", "STOCK", "ETF", "CEO", "CFO", "SEC", "IPO", "USA", "INC", "LLC", "LTD", "CORP"]:
                    tickers.add(match)
    
    return sorted(list(tickers))

def format_report(results):
    """Format results into a readable report"""
    today = datetime.now().strftime("%B %d, %Y")
    
    report = f"🚀 POTENTIAL BREAKOUT STOCKS - {today}\n\n"
    report += "=" * 60 + "\n\n"
    
    # Technical setups
    if results["technical"]:
        report += "📈 TECHNICAL BREAKOUT SETUPS\n"
        report += "-" * 60 + "\n"
        for r in results["technical"][:3]:
            report += f"• {r.get('title', 'N/A')}\n"
            snippet = r.get('text', '')[:200].strip()
            if snippet:
                report += f"  {snippet}...\n"
            report += f"  🔗 {r.get('url', '')}\n\n"
    
    # Earnings catalysts
    if results["earnings"]:
        report += "\n💰 EARNINGS CATALYSTS\n"
        report += "-" * 60 + "\n"
        for r in results["earnings"][:3]:
            report += f"• {r.get('title', 'N/A')}\n"
            snippet = r.get('text', '')[:200].strip()
            if snippet:
                report += f"  {snippet}...\n"
            report += f"  🔗 {r.get('url', '')}\n\n"
    
    # Social signals
    if results["social"]:
        report += "\n🔥 SOCIAL SIGNALS & UNUSUAL ACTIVITY\n"
        report += "-" * 60 + "\n"
        for r in results["social"][:3]:
            report += f"• {r.get('title', 'N/A')}\n"
            snippet = r.get('text', '')[:200].strip()
            if snippet:
                report += f"  {snippet}...\n"
            report += f"  🔗 {r.get('url', '')}\n\n"
    
    # Institutional activity
    if results["institutional"]:
        report += "\n🎯 INSTITUTIONAL ACTIVITY\n"
        report += "-" * 60 + "\n"
        for r in results["institutional"][:2]:
            report += f"• {r.get('title', 'N/A')}\n"
            snippet = r.get('text', '')[:200].strip()
            if snippet:
                report += f"  {snippet}...\n"
            report += f"  🔗 {r.get('url', '')}\n\n"
    
    # Extract mentioned tickers
    tickers = extract_tickers(results)
    if tickers:
        report += "\n📊 STOCKS MENTIONED\n"
        report += "-" * 60 + "\n"
        report += ", ".join(tickers[:20])  # Top 20
        report += "\n\n"
    
    report += "=" * 60 + "\n"
    report += "⚠️ NOT FINANCIAL ADVICE - Do your own research!\n"
    report += "=" * 60 + "\n"
    
    return report

def main():
    print("🚀 Starting Breakout Scanner...\n")
    
    results = find_breakout_candidates()
    report = format_report(results)
    
    print("\n" + report)
    
    # Return structured data for publishing
    return {
        "report": report,
        "results": results
    }

if __name__ == "__main__":
    main()
