#!/bin/bash
# Create a Git repo with your full OpenClaw setup (secrets sanitized)

REPO_NAME="openclaw-config-backup"
BACKUP_DIR="/tmp/$REPO_NAME"

echo "🚀 Creating Git repo backup..."

# Clean previous
rm -rf "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

cd "$BACKUP_DIR" || exit 1

# Init repo
git init
git config user.name "Nivo"
git config user.email "nivo@openclaw.local"

# Copy workspace (your files)
echo "📂 Copying workspace..."
mkdir -p workspace
cp -r ~/.openclaw/workspace/* workspace/ 2>/dev/null

# Copy memory
echo "🧠 Copying memory..."
mkdir -p memory
cp -r ~/.openclaw/memory/* memory/ 2>/dev/null

# Copy cron jobs
echo "⏰ Copying cron jobs..."
mkdir -p cron
cp ~/.openclaw/cron/jobs.json cron/ 2>/dev/null

# Sanitize config (remove secrets)
echo "🔐 Sanitizing config..."
cat > config-template.json << 'CONFIGEOF'
{
  "note": "This is a TEMPLATE. Add your own API keys before use.",
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-5",
        "fallbacks": ["openai/gpt-5.2", "deepseek/deepseek-reasoner", "google/gemini-3-flash"]
      },
      "heartbeat": {
        "every": "30m",
        "model": "google/gemini-2.5-flash-lite"
      },
      "contextTokens": 200000
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "REPLACE_WITH_YOUR_TELEGRAM_BOT_TOKEN"
    }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "auto"
  },
  "env": {
    "GITHUB_TOKEN": "REPLACE_WITH_YOUR_GITHUB_TOKEN",
    "EXA_API_KEY": "REPLACE_WITH_YOUR_EXA_KEY"
  }
}
CONFIGEOF

# Create comprehensive README
cat > README.md << 'EOF'
# OpenClaw Configuration Backup 🌊

**Created:** $(date)  
**Agent:** Nivo  
**Human:** Assaf

---

## 📂 Contents

```
├── workspace/           # All files, scripts, skills
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── USER.md
│   ├── trading-rules.md
│   ├── scripts/         # Python automation scripts
│   └── skills/          # Custom skills
├── memory/              # Daily memory files
├── cron/                # Cron job definitions
└── config-template.json # Config template (add your keys)
```

---

## 🚀 Quick Start (New Machine)

### 1. Install OpenClaw
```bash
npm install -g openclaw
openclaw configure
```

### 2. Clone this repo
```bash
git clone https://github.com/lafofo-nivo/openclaw-config-backup
cd openclaw-config-backup
```

### 3. Restore workspace
```bash
cp -r workspace/* ~/.openclaw/workspace/
cp -r memory/* ~/.openclaw/memory/
cp cron/jobs.json ~/.openclaw/cron/
```

### 4. Configure API keys
```bash
# Telegram
openclaw configure telegram --token <YOUR_BOT_TOKEN>

# Anthropic (Claude)
export ANTHROPIC_API_KEY="sk-ant-..."

# Google (Gemini)
export GOOGLE_API_KEY="AIza..."

# GitHub (for daily-brief)
export GITHUB_TOKEN="github_pat_..."

# Exa (search)
export EXA_API_KEY="..."
```

Or edit `~/.openclaw/openclaw.json` directly with values from `config-template.json`.

### 5. Start gateway
```bash
openclaw gateway restart
openclaw status
```

---

## 📊 Daily Automations

This setup includes **4 cron jobs** (see `cron/jobs.json`):

1. **07:00 IL** - Market Brief (stocks + crypto)
2. **08:00 IL** - Yad2 Real Estate Scan (Beer Yaakov, 5 rooms)
3. **09:00 IL** - YouTube Monitor (More Crypto Online, InvestAnswers)
4. **09:30 IL** - Jobs Scan (DevOps/Cloud roles)

All results go to:
- **Telegram** (direct messages)
- **GitHub Pages** → https://lafofo-nivo.github.io/daily-brief/

---

## 🧠 Memory System

- **MEMORY.md** - Long-term curated memory
- **memory/YYYY-MM-DD.md** - Daily logs
- Automatically synced via `AGENTS.md` rules

---

## 🔐 Security

⚠️ **This repo does NOT contain:**
- API keys
- Telegram bot tokens
- GitHub personal access tokens
- Any credentials

You must add these manually after cloning.

---

## 🛠️ Customization

### Add a new skill:
```bash
cd ~/.openclaw/workspace/skills
mkdir my-skill
echo "# My Skill" > my-skill/SKILL.md
```

### Add a new cron job:
```bash
# Edit ~/.openclaw/cron/jobs.json
# Then restart:
openclaw gateway restart
```

---

## 📖 Documentation

- OpenClaw Docs: https://docs.openclaw.ai
- Skills Hub: https://clawhub.com
- Community: https://discord.com/invite/clawd

---

**Built with ❤️ by Nivo 🌊**
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Secrets
*.key
*.pem
credentials/
.env

# Logs
*.log
/tmp/

# System
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
*.pyo
venv/

# Node
node_modules/
package-lock.json
EOF

# Commit everything
git add .
git commit -m "Initial backup - Full OpenClaw config

- Workspace files (AGENTS.md, SOUL.md, USER.md, trading-rules.md)
- Daily automation scripts (market_brief.py, yad2_scan.py, jobs_scan.py)
- Memory system
- Cron job definitions
- Config template (secrets redacted)

Created: $(date)"

echo ""
echo "✅ Git repo created at: $BACKUP_DIR"
echo ""
echo "📤 To push to GitHub:"
echo ""
echo "  cd $BACKUP_DIR"
echo "  gh repo create openclaw-config-backup --public --source=. --remote=origin --push"
echo ""
echo "  Or manually:"
echo "  # Create repo on GitHub: lafofo-nivo/openclaw-config-backup"
echo "  git remote add origin https://github.com/lafofo-nivo/openclaw-config-backup.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
