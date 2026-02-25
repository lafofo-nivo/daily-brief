#!/usr/bin/env python3
"""
Exa web search. Uses EXA_API_KEY env var or --api-key flag.
Usage:
  python3 exa_search.py "your query" [options]

Options:
  --api-key KEY          Exa API key (or set EXA_API_KEY env var)
  --num NUM              Number of results (default: 5)
  --type TYPE            Search type: neural|keyword|auto (default: auto)
  --start-date DATE      Filter by published date start (YYYY-MM-DD)
  --end-date DATE        Filter by published date end (YYYY-MM-DD)
  --include-domains D    Comma-separated domains to include (e.g. reddit.com,github.com)
  --exclude-domains D    Comma-separated domains to exclude
  --text                 Include full text content in results
  --highlights           Include highlighted excerpts
"""
import argparse, json, os, sys
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--api-key", default=os.environ.get("EXA_API_KEY", ""))
    parser.add_argument("--num", type=int, default=5)
    parser.add_argument("--type", default="auto", choices=["neural","keyword","auto"])
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--include-domains")
    parser.add_argument("--exclude-domains")
    parser.add_argument("--text", action="store_true")
    parser.add_argument("--highlights", action="store_true")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: EXA_API_KEY not set. Pass --api-key or set the env var.", file=sys.stderr)
        sys.exit(1)

    payload = {
        "query": args.query,
        "numResults": args.num,
        "type": args.type,
        "useAutoprompt": True,
    }
    if args.start_date:
        payload["startPublishedDate"] = args.start_date + "T00:00:00.000Z"
    if args.end_date:
        payload["endPublishedDate"] = args.end_date + "T23:59:59.000Z"
    if args.include_domains:
        payload["includeDomains"] = args.include_domains.split(",")
    if args.exclude_domains:
        payload["excludeDomains"] = args.exclude_domains.split(",")

    contents = {}
    if args.text:
        contents["text"] = {"maxCharacters": 2000}
    if args.highlights:
        contents["highlights"] = {"numSentences": 3}
    if contents:
        payload["contents"] = contents

    resp = requests.post(
        "https://api.exa.ai/search",
        headers={"x-api-key": args.api_key, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    for i, r in enumerate(data.get("results", []), 1):
        print(f"\n[{i}] {r.get('title', 'No title')}")
        print(f"    URL: {r.get('url')}")
        if r.get("publishedDate"):
            print(f"    Date: {r['publishedDate'][:10]}")
        if r.get("author"):
            print(f"    Author: {r['author']}")
        if r.get("text"):
            snippet = r["text"][:300].replace("\n", " ")
            print(f"    Text: {snippet}...")
        if r.get("highlights"):
            for h in r["highlights"][:2]:
                print(f"    > {h}")

if __name__ == "__main__":
    main()
