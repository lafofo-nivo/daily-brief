#!/usr/bin/env python3
"""
Exa company research — gather info about a company from multiple angles.
Usage:
  python3 exa_company.py "Company Name" [--api-key KEY] [--num N]
"""
import argparse, os, sys
import requests

def search(api_key, query, num=3, include_domains=None):
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
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])

def print_results(label, results):
    print(f"\n=== {label} ===")
    if not results:
        print("  (no results)")
        return
    for r in results:
        print(f"  [{r.get('title', 'N/A')}]")
        print(f"  {r.get('url')}")
        if r.get("text"):
            print(f"  {r['text'][:250].replace(chr(10), ' ')}...")
        print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("company")
    parser.add_argument("--api-key", default=os.environ.get("EXA_API_KEY", ""))
    parser.add_argument("--num", type=int, default=3)
    args = parser.parse_args()

    if not args.api_key:
        print("Error: EXA_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    name = args.company
    print(f"Researching: {name}\n")

    print_results("Overview", search(args.api_key, f"{name} company overview what they do", args.num))
    print_results("News & Recent", search(args.api_key, f"{name} latest news 2024 2025", args.num))
    print_results("Funding & Business", search(args.api_key, f"{name} funding revenue business model", args.num,
                  include_domains=["crunchbase.com", "techcrunch.com", "pitchbook.com", "businessinsider.com"]))

if __name__ == "__main__":
    main()
