#!/usr/bin/env python3
"""
Daily job scanner for Assaf — Infrastructure Architect / DevOps / Cloud roles in Israel.
Sources: LinkedIn, Drushim, AllJobs, JobMaster.
"""
import os, sys, json, requests, hashlib
from datetime import date
from pathlib import Path

EXA_API_KEY = os.environ.get("EXA_API_KEY", "8fc77e5d-5509-43d1-983b-2be228275afb")
STATE_FILE = Path(__file__).parent.parent / "data" / "jobs_seen.json"
STATE_FILE.parent.mkdir(exist_ok=True)

SEARCHES = [
    {
        "query": "Infrastructure Architect DevOps Cloud jobs Israel 2026",
        "domains": ["il.linkedin.com", "linkedin.com"],
        "label": "LinkedIn IL"
    },
    {
        "query": "ארכיטקט תשתיות דבאופס ענן משרה ישראל 2026",
        "domains": ["drushim.co.il", "alljobs.co.il", "jobmaster.co.il", "il.linkedin.com"],
        "label": "Israeli Job Boards"
    },
    {
        "query": "Senior DevOps Engineer Platform Engineer Israel remote hybrid 2026",
        "domains": ["il.linkedin.com", "linkedin.com", "glassdoor.com"],
        "label": "Senior DevOps"
    },
    {
        "query": "Cloud Architect AWS Azure GCP Israel 2026 hiring",
        "domains": ["il.linkedin.com", "linkedin.com"],
        "label": "Cloud Architect"
    },
]

def search(query, domains, num=5):
    resp = requests.post(
        "https://api.exa.ai/search",
        headers={"x-api-key": EXA_API_KEY, "Content-Type": "application/json"},
        json={
            "query": query,
            "numResults": num,
            "type": "neural",
            "useAutoprompt": True,
            "includeDomains": domains,
            "contents": {"text": {"maxCharacters": 400}},
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])

def make_id(url):
    return hashlib.md5(url.encode()).hexdigest()[:12]

def load_seen():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_seen(seen):
    STATE_FILE.write_text(json.dumps(seen, indent=2))

def main():
    today = date.today().strftime("%d/%m/%Y")
    seen = load_seen()
    new_jobs = []

    for s in SEARCHES:
        try:
            results = search(s["query"], s["domains"])
        except Exception as e:
            print(f"Error in {s['label']}: {e}", file=sys.stderr)
            continue

        for r in results:
            url = r.get("url", "")
            title = r.get("title", "").strip()
            uid = make_id(url)

            if uid in seen:
                continue
            if not any(kw in (title + url).lower() for kw in
                       ["devops", "infrastructure", "cloud", "architect", "sre", "platform", "reliability", "kubernetes", "k8s"]):
                seen[uid] = {"title": title, "skipped": True}
                continue

            snippet = r.get("text", "")[:300].replace("\n", " ").strip() if r.get("text") else ""
            job = {
                "uid": uid,
                "title": title,
                "url": url,
                "source": s["label"],
                "snippet": snippet,
                "date": today,
            }
            new_jobs.append(job)
            seen[uid] = {"title": title, "sent": True, "date": today}
            print(f"🆕 {title}\n   🔗 {url}\n   {snippet[:150]}...\n")

    save_seen(seen)

    if not new_jobs:
        print(f"No new relevant jobs found today ({today}).")

    return new_jobs

if __name__ == "__main__":
    main()
