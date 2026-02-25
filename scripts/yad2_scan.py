#!/usr/bin/env python3
"""
Daily Yad2 scanner for Assaf - 5 room apartments in Be'er Ya'akov
Scans both rent and sale listings and prints a summary.
"""
import os, sys, json, re, requests
from datetime import date

EXA_API_KEY = os.environ.get("EXA_API_KEY", "8fc77e5d-5509-43d1-983b-2be228275afb")

RENT_URL = "https://www.yad2.co.il/realestate/rent?area=9&city=2530&property=1&propertyGroup=apartments&rooms=5-5&topArea=2&maxPrice=9000&balcony=1&parking=1&storage=1"
SALE_URL = "https://www.yad2.co.il/realestate/forsale?area=9&city=2530&property=1&propertyGroup=apartments&rooms=5-5&topArea=2&balcony=1&parking=1&storage=1"

def crawl(url):
    resp = requests.post(
        "https://api.exa.ai/contents",
        headers={"x-api-key": EXA_API_KEY, "Content-Type": "application/json"},
        json={"ids": [url], "text": {"maxCharacters": 15000}},
        timeout=30,
    )
    resp.raise_for_status()
    results = resp.json().get("results", [])
    return results[0].get("text", "") if results else ""

def parse_listings(text):
    listings = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        # Listings look like: ## כתובתדירה, שכונה, באר יעקב5 חדרים • קומה X • Y מ״ר
        if line.startswith("## ") and "דירה," in line and "5 חדרים" in line and "באר יעקב" in line:
            details = line[3:].strip()
            # Price is on the line before
            price = ""
            for j in range(i-1, max(i-5, 0), -1):
                if "₪" in lines[j]:
                    price = lines[j].strip()
                    break
            # Clean price - extract just the ₪ and number
            m = re.search(r'₪[\s\d,]+', price)
            clean_price = m.group(0).strip() if m else price
            listings.append({
                "details": details,
                "price": clean_price or "מחיר לא צוין"
            })
    return listings

def main():
    today = date.today().strftime("%d/%m/%Y")
    print(f"🏠 סריקת יד2 - {today}")
    print("=" * 40)

    # Rent
    print("\n📋 להשכרה | 5 חדרים | עד ₪9,000 | חניה+מחסן+מרפסת | באר יעקב\n")
    rent_text = crawl(RENT_URL)
    rent_listings = parse_listings(rent_text)
    if rent_listings:
        for l in rent_listings:
            print(f"📍 {l['details']}")
            print(f"   💰 {l['price']}")
            print()
    else:
        print("לא נמצאו מודעות להשכרה.\n")

    # Sale
    print("\n🏡 למכירה | 5 חדרים | חניה+מחסן+מרפסת | באר יעקב\n")
    sale_text = crawl(SALE_URL)
    sale_listings = parse_listings(sale_text)
    if sale_listings:
        for l in sale_listings[:8]:  # top 8
            print(f"📍 {l['details']}")
            print(f"   💰 {l['price']}")
            print()
    else:
        print("לא נמצאו מודעות למכירה.\n")

    print(f"\n🔗 השכרה: {RENT_URL}")
    print(f"🔗 מכירה: {SALE_URL}")

if __name__ == "__main__":
    main()
