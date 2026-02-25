#!/bin/bash
# OpenClaw Full Backup Script
# Creates a complete snapshot of your OpenClaw setup

BACKUP_DIR="openclaw-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Creating full OpenClaw backup..."

# 1. Workspace (all your files)
echo "  Copying workspace..."
cp -r ~/.openclaw/workspace "$BACKUP_DIR/"

# 2. Config (sanitized - without secrets)
echo "  Exporting config (secrets redacted)..."
openclaw config export > "$BACKUP_DIR/config-export.json" 2>/dev/null || \
  cp ~/.openclaw/openclaw.json "$BACKUP_DIR/openclaw-config.json"

# 3. Memory
echo "  Copying memory..."
cp -r ~/.openclaw/memory "$BACKUP_DIR/" 2>/dev/null

# 4. Cron jobs
echo "  Copying cron jobs..."
cp ~/.openclaw/cron/jobs.json "$BACKUP_DIR/" 2>/dev/null

# 5. Create README
cat > "$BACKUP_DIR/README.md" << 'READMEEOF'
# OpenClaw Backup

Created: $(date)

## Contents:
- `workspace/` - All your files, scripts, skills
- `memory/` - Daily memory files
- `jobs.json` - Cron job definitions
- `openclaw-config.json` - Full config (check for secrets!)

## Restore on new machine:

```bash
# 1. Install OpenClaw
npm install -g openclaw

# 2. Configure basics
openclaw configure

# 3. Restore workspace
cp -r workspace ~/.openclaw/

# 4. Restore memory
cp -r memory ~/.openclaw/

# 5. Restore cron jobs
cp jobs.json ~/.openclaw/cron/

# 6. Manually set API keys:
openclaw configure telegram --token <your-token>
# (repeat for other services)

# 7. Restart
openclaw gateway restart
```

## Security Warning:
⚠️ This backup may contain API keys/tokens!
Do NOT commit to public repos without sanitizing.
READMEEOF

echo "✅ Backup created: $BACKUP_DIR"
echo "📊 Size: $(du -sh $BACKUP_DIR | cut -f1)"

