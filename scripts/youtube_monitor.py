#!/usr/bin/env python3
"""
YouTube channel monitor — More Crypto Online (@morecryptoonline)
Watches for new SOL/BTC videos and summarizes them.
Sends to Telegram via OpenClaw.
"""
import os, sys, json, urllib.request, xml.etree.ElementTree as ET, requests
from datetime import datetime, timezone
from pathlib import Path

EXA_API_KEY = os.environ.get("EXA_API_KEY", "8fc77e5d-5509-43d1-983b-2be228275afb")
STATE_FILE = Path(__file__).parent.parent / "data" / "youtube_seen.json"
STATE_FILE.parent.mkdir(exist_ok=True)

CHANNELS = [
    {
        "name": "More Crypto Online",
        "channel_id": "UCngIhBkikUe6e7tZTjpKK7Q",
        "filter_keywords": ["bitcoin", "btc", "solana", "sol"],
    },
    {
        "name": "InvestAnswers",
        "channel_id": "UClgJyzwGs-GyaNxUHcLZrkg",
        "filter_keywords": None,  # All videos
    },
]

KEYWORDS = ["bitcoin", "btc", "solana", "sol"]

def load_seen():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_seen(seen):
    STATE_FILE.write_text(json.dumps(seen, indent=2))

def fetch_feed(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    with urllib.request.urlopen(url, timeout=15) as r:
        return r.read()

def parse_feed(xml_data):
    root = ET.fromstring(xml_data)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/",
    }
    videos = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text or ""
        link = entry.find("atom:link", ns).get("href", "")
        video_id = entry.find("yt:videoId", ns).text or ""
        published = entry.find("atom:published", ns).text or ""
        description_el = entry.find(".//media:description", ns)
        description = description_el.text[:500] if description_el is not None and description_el.text else ""
        videos.append({
            "id": video_id,
            "title": title,
            "url": link,
            "published": published[:10],
            "description": description,
        })
    return videos

def is_relevant(video, keywords):
    if keywords is None:
        return True  # No filter — all videos pass
    text = (video["title"] + " " + video["description"]).lower()
    return any(kw in text for kw in keywords)

def summarize_video(video):
    """Use Exa to crawl the video page for more context."""
    try:
        resp = requests.post(
            "https://api.exa.ai/contents",
            headers={"x-api-key": EXA_API_KEY, "Content-Type": "application/json"},
            json={"ids": [video["url"]], "text": {"maxCharacters": 1500}},
            timeout=20,
        )
        results = resp.json().get("results", [])
        if results and results[0].get("text"):
            return results[0]["text"][:800]
    except Exception:
        pass
    return video["description"]

def format_message(channel_name, video, summary):
    coin = "₿ BTC" if any(k in (video["title"] + video["description"]).lower() for k in ["bitcoin", "btc"]) else "◎ SOL"
    return (
        f"📺 *{channel_name}* — New Video\n\n"
        f"{coin} *{video['title']}*\n"
        f"📅 {video['published']}\n\n"
        f"_{summary[:400]}_\n\n"
        f"🔗 {video['url']}"
    )

def main():
    seen = load_seen()
    new_videos = []

    for channel in CHANNELS:
        try:
            xml_data = fetch_feed(channel["channel_id"])
            videos = parse_feed(xml_data)
        except Exception as e:
            print(f"Error fetching {channel['name']}: {e}", file=sys.stderr)
            continue

        for video in videos:
            if video["id"] in seen:
                continue
            if not is_relevant(video, channel["filter_keywords"]):
                seen[video["id"]] = {"title": video["title"], "skipped": True}
                continue

            # New relevant video!
            summary = summarize_video(video)
            msg = format_message(channel["name"], video, summary)
            new_videos.append(msg)
            seen[video["id"]] = {"title": video["title"], "sent": True, "date": video["published"]}
            print(msg)
            print("---")

    save_seen(seen)

    if not new_videos:
        print("No new relevant videos.")

if __name__ == "__main__":
    main()
