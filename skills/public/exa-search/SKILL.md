---
name: exa-search
description: Advanced web search, URL crawling, people search, company research, and deep AI-powered research using Exa. Use when the user asks to search the web with quality results, find LinkedIn/professional profiles, research a person or company, crawl a specific URL for content, or start a deep research report on any topic.
---

# Exa Search

Exa provides neural (semantic) web search with full content access. All tools require `EXA_API_KEY` set in env (configured in openclaw.json).

## Scripts

All scripts live in `scripts/` and are run via `exec`. Pass `--api-key $EXA_API_KEY` or rely on the env var.

### Web Search
```bash
python3 skills/public/exa-search/scripts/exa_search.py "query" [--num 5] [--type auto|neural|keyword] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD] [--include-domains a.com,b.com] [--text] [--highlights]
```

### Crawl a URL
```bash
python3 skills/public/exa-search/scripts/exa_crawl.py "https://example.com" [--max-chars 5000]
```

### People Search (LinkedIn, Twitter, GitHub, etc.)
```bash
python3 skills/public/exa-search/scripts/exa_people.py "First Last" [--num 5] [--domains linkedin.com,twitter.com]
```

### Company Research
```bash
python3 skills/public/exa-search/scripts/exa_company.py "Company Name" [--num 3]
```

## Workflow Tips

- **People search**: Always use `exa_people.py` — it targets professional networks automatically.
- **Deep research**: Chain `exa_search.py` → `exa_crawl.py` on top results to synthesize a report.
- **Date filtering**: Use `--start-date` / `--end-date` for recent news or research.
- **Domain filtering**: Use `--include-domains` to restrict to trusted sources.

## API Reference
See [references/api_reference.md](references/api_reference.md) for full parameter details.
