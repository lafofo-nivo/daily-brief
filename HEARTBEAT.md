# HEARTBEAT.md

## Daily Brief Automation (Run 2x/day: 08:00 & 16:00 UTC)

### Morning Check (08:00 UTC):
1. **YouTube Monitor:** `cd scripts && python3 youtube_monitor.py` → publish new BTC/SOL videos
2. **Yad2 Scan:** `cd scripts && python3 yad2_scan.py` → publish Be'er Ya'akov listings
3. **Breakout Scanner:** `cd scripts && python3 breakout_publisher.py` → publish stocks with breakout potential
4. Publish all to https://lafofo-nivo.github.io/daily-brief/

### Afternoon Check (16:00 UTC):
1. Check for new YouTube videos
2. Re-scan breakouts (markets move fast!)
3. Send weather + daily tasks summary to Telegram (NOT to site)

**Remember:** 
- Site gets: Crypto/YouTube/Yad2/Jobs
- Telegram gets: Weather/tasks/personal updates

---

## Current Focus: RESEARCH SPRINT (Feb 24-27)

### Daily Research Tasks (30-60 min per heartbeat)
Follow `projects/RESEARCH-SPRINT.md` day-by-day:

**Day 1 (Feb 24):** ✅ COMPLETE - Bookkeeping market (see `projects/DAY1-SUMMARY.md`)
**Day 2 (Feb 25):** Bot services market sizing + pain points + competitors  
**Day 3 (Feb 26):** Niche hunting in both markets (3-5 micro-niches each)
**Day 4 (Feb 27):** Customer interviews + final scoring + recommendation

Each evening: Post summary to Assaf (key findings + early insights)

Stay silent during research unless something critical/exciting emerges.
