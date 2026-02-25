#!/usr/bin/env python3
"""
Daily market brief for Assaf.
Focuses on: stock breakouts, crypto moves, key catalysts.
High signal, low noise.
"""
import os, re, requests
from datetime import date

EXA_API_KEY = os.environ.get("EXA_API_KEY", "8fc77e5d-5509-43d1-983b-2be228275afb")

def search(query, num=4, include_domains=None, hours_back=24):
    payload = {
        "query": query,
        "numResults": num,
        "type": "neural",
        "useAutoprompt": True,
        "contents": {"text": {"maxCharacters": 600}},
    }
    if include_domains:
        payload["includeDomains"] = include_domains
    resp = requests.post(
        "https://api.exa.ai/search",
        headers={"x-api-key": EXA_API_KEY, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])

def print_section(title, results):
    print(f"\n{'='*40}")
    print(f"  {title}")
    print(f"{'='*40}")
    if not results:
        print("  No significant results.")
        return
    for r in results:
        print(f"\n📌 {r.get('title', '')}")
        print(f"   🔗 {r.get('url', '')}")
        if r.get("publishedDate"):
            print(f"   🕐 {r['publishedDate'][:10]}")
        if r.get("text"):
            snippet = r["text"][:250].replace("\n", " ").strip()
            print(f"   {snippet}...")

def main():
    today = date.today().strftime("%A, %B %d %Y")
    print(f"\n🌊 MARKET BRIEF — {today}")

    # 1. Stock breakouts & big movers
    print_section("📈 STOCK BREAKOUTS & BIG MOVERS", search(
        "stocks breaking out 52-week high unusual volume today",
        num=4,
        include_domains=["finviz.com", "investors.com", "marketwatch.com", "benzinga.com", "stockanalysis.com"]
    ))

    # 2. Crypto — big moves & catalysts
    print_section("₿ CRYPTO — KEY MOVES & CATALYSTS", search(
        "bitcoin ethereum crypto breakout catalyst news today",
        num=4,
        include_domains=["coindesk.com", "cointelegraph.com", "theblock.co", "decrypt.co"]
    ))

    # 3. High-impact events (earnings, FDA, macro)
    print_section("⚡ CATALYSTS TO WATCH", search(
        "market moving catalyst earnings FDA approval macro event this week",
        num=4,
        include_domains=["benzinga.com", "seekingalpha.com", "marketwatch.com", "reuters.com", "bloomberg.com"]
    ))

    # 4. One contrarian / under-the-radar pick
    print_section("🔍 UNDER THE RADAR", search(
        "undervalued stock hidden gem unusual options activity smart money",
        num=3,
        include_domains=["seekingalpha.com", "investors.com", "benzinga.com", "unusual-whales.com"]
    ))

    print(f"\n{'='*40}")
    print("  Stay sharp. Trade the setup, not the hype. 🌊")
    print(f"{'='*40}\n")

if __name__ == "__main__":
    main()
