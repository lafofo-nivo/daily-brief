---
name: auto-backup
description: Automatic backup of conversations, context, and workspace to markdown files with Git sync. Use when user asks to backup, save context, sync to git, or for periodic automated backups.
author: nivo
version: 1.0.0
emoji: 💾
tags: [backup, git, sync, memory, automation]
---

# Auto Backup Skill

Automatically backs up conversations, context, memory, and workspace files to a Git repository.

## What Gets Backed Up

- **Daily Logs**: `logs/YYYY-MM-DD.md` - All conversations and requests
- **Memory**: `memory/` - Daily memory files
- **Workspace**: `workspace/` - All workspace files (AGENTS.md, SOUL.md, scripts, skills)
- **Config**: `config-template.json` - Sanitized config (no secrets)
- **Cron**: `cron/jobs.json` - Scheduled jobs

## Directory Structure

```
~/.openclaw/backup/
├── logs/
│   └── YYYY-MM-DD.md      # Daily conversation logs
├── memory/
│   └── YYYY-MM-DD.md      # Memory files
├── workspace/
│   └── ...                 # Full workspace mirror
├── cron/
│   └── jobs.json
└── config-template.json
```

## Usage

### Manual Backup
When user says "backup", "גיבוי", "save context", or "sync to git":

```bash
# Run full backup + git sync
bash ~/.openclaw/workspace/skills/auto-backup/scripts/backup_and_sync.sh
```

### Log Current Conversation
To append current context to today's log:

```bash
python3 ~/.openclaw/workspace/skills/auto-backup/scripts/log_context.py "Summary of conversation or request"
```

### Just Git Sync (no new backup)
```bash
bash ~/.openclaw/workspace/skills/auto-backup/scripts/git_sync.sh
```

## Automatic Backup (Cron/Heartbeat)

Add to HEARTBEAT.md for periodic backups:
```markdown
## Backup Check
Every 4-6 hours, run auto-backup if significant changes occurred.
```

Or create a cron job:
```bash
openclaw cron add --schedule "0 */6 * * *" --task "Run auto-backup skill - sync workspace to git"
```

## Git Setup (First Time)

1. Create a **private** GitHub repo (e.g., `openclaw-backup`)
2. Set GITHUB_TOKEN with repo access
3. Run initial setup:

```bash
cd ~/.openclaw/backup
git init
git remote add origin https://github.com/YOUR_USER/openclaw-backup.git
git branch -M main
```

## Instructions for Model

When user requests backup:

1. **Quick backup**: Run `backup_and_sync.sh`
2. **Log specific context**: Use `log_context.py` with summary
3. **Check status**: `cd ~/.openclaw/backup && git status`
4. **View recent logs**: `cat ~/.openclaw/backup/logs/$(date +%Y-%m-%d).md`

Always confirm what was backed up and whether git push succeeded.
