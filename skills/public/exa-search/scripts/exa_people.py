#!/usr/bin/env python3
"""
Exa people search — find professional profiles for a person.
Usage:
  python3 exa_people.py "First Last" [--api-key KEY] [--num N]
"""
import argparse, os, sys
import requests

PEOPLE_DOMAINS = [
    "linkedin.com", "twitter.com", "github.com", "about.me",
    "angel.co", "crunchbase.com", "wellfound.com"
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--api-key", default=os.environ.get("EXA_API_KEY", ""))
    parser.add_argument("--num", type=int, default=5)
    parser.add_argument("--domains", help="Comma-separated domains to search in (default: LinkedIn, Twitter, GitHub etc.)")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: EXA_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    include_domains = args.domains.split(",") if args.domains else PEOPLE_DOMAINS

    query = f"{args.name} professional profile"
    resp = requests.post(
        "https://api.exa.ai/search",
        headers={"x-api-key": args.api_key, "Content-Type": "application/json"},
        json={
            "query": query,
            "numResults": args.num,
            "type": "neural",
            "useAutoprompt": True,
            "includeDomains": include_domains,
            "contents": {
                "text": {"maxCharacters": 500},
            }
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    results = data.get("results", [])
    if not results:
        print(f"No profiles found for '{args.name}'.")
        return

    print(f"Profiles found for: {args.name}\n")
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r.get('title', 'No title')}")
        print(f"    URL: {r.get('url')}")
        if r.get("text"):
            snippet = r["text"][:300].replace("\n", " ")
            print(f"    Bio: {snippet}...")
        print()

if __name__ == "__main__":
    main()
