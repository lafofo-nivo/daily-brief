#!/usr/bin/env python3
"""
Exa URL crawler — fetch clean text from a specific URL.
Usage:
  python3 exa_crawl.py <url> [--api-key KEY] [--max-chars N]
"""
import argparse, os, sys
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--api-key", default=os.environ.get("EXA_API_KEY", ""))
    parser.add_argument("--max-chars", type=int, default=5000)
    args = parser.parse_args()

    if not args.api_key:
        print("Error: EXA_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    resp = requests.post(
        "https://api.exa.ai/contents",
        headers={"x-api-key": args.api_key, "Content-Type": "application/json"},
        json={
            "ids": [args.url],
            "text": {"maxCharacters": args.max_chars},
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    for r in data.get("results", []):
        print(f"Title: {r.get('title', 'N/A')}")
        print(f"URL: {r.get('url')}")
        if r.get("publishedDate"):
            print(f"Date: {r['publishedDate'][:10]}")
        print(f"\n--- Content ---\n")
        print(r.get("text", "(no text returned)"))

if __name__ == "__main__":
    main()
