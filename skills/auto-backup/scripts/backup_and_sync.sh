#!/bin/bash
# Full backup + Git sync
# Backs up workspace, memory, cron, config to ~/.openclaw/backup and pushes to git

set -e

BACKUP_DIR="$HOME/.openclaw/backup"
WORKSPACE="$HOME/.openclaw/workspace"
MEMORY="$HOME/.openclaw/memory"
CRON="$HOME/.openclaw/cron"
CONFIG="$HOME/.openclaw/openclaw.json"

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)

echo "💾 Starting full backup..."
echo "   Date: $DATE $TIME"

# Create backup directories
mkdir -p "$BACKUP_DIR"/{logs,memory,workspace,cron}

# 1. Backup workspace (excluding .git and large files)
echo "📂 Backing up workspace..."
rm -rf "$BACKUP_DIR/workspace"
mkdir -p "$BACKUP_DIR/workspace"
cd "$WORKSPACE"
find . -type f \
    ! -path './.git/*' \
    ! -path './node_modules/*' \
    ! -path './__pycache__/*' \
    ! -name '*.pyc' \
    ! -name '.env' \
    -exec cp --parents {} "$BACKUP_DIR/workspace/" \;

# 2. Backup memory
echo "🧠 Backing up memory..."
if [ -d "$MEMORY" ]; then
    cp -r "$MEMORY"/* "$BACKUP_DIR/memory/" 2>/dev/null || true
fi

# 3. Backup cron jobs
echo "⏰ Backing up cron jobs..."
if [ -f "$CRON/jobs.json" ]; then
    cp "$CRON/jobs.json" "$BACKUP_DIR/cron/"
fi

# 4. Create sanitized config (remove secrets)
echo "🔐 Creating sanitized config..."
if [ -f "$CONFIG" ]; then
    # Remove sensitive keys but keep structure
    cat "$CONFIG" | python3 -c "
import sys, json
config = json.load(sys.stdin)
def sanitize(obj, path=''):
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            key_lower = k.lower()
            if any(s in key_lower for s in ['token', 'key', 'secret', 'password', 'credential']):
                if isinstance(v, str) and len(v) > 4:
                    obj[k] = v[:4] + '...[REDACTED]'
            else:
                sanitize(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for item in obj:
            sanitize(item, path)
sanitize(config)
print(json.dumps(config, indent=2))
" > "$BACKUP_DIR/config-template.json" 2>/dev/null || echo '{}' > "$BACKUP_DIR/config-template.json"
fi

# 5. Add backup log entry
LOG_FILE="$BACKUP_DIR/logs/$DATE.md"
if [ ! -f "$LOG_FILE" ]; then
    echo "# Log - $DATE" > "$LOG_FILE"
    echo "" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "## [$TIME] Auto Backup" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "- Workspace: $(find "$BACKUP_DIR/workspace" -type f | wc -l) files" >> "$LOG_FILE"
echo "- Memory: $(find "$BACKUP_DIR/memory" -type f 2>/dev/null | wc -l) files" >> "$LOG_FILE"
echo "- Cron jobs: $(cat "$BACKUP_DIR/cron/jobs.json" 2>/dev/null | grep -c '"id"' || echo 0)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

# 6. Update README
cat > "$BACKUP_DIR/README.md" << 'EOF'
# OpenClaw Backup 💾

Auto-generated backup of OpenClaw configuration and context.

## Contents

- `logs/` - Daily conversation logs (YYYY-MM-DD.md)
- `memory/` - Memory files
- `workspace/` - Full workspace (AGENTS.md, SOUL.md, scripts, skills)
- `cron/` - Scheduled jobs
- `config-template.json` - Sanitized config (secrets redacted)

## Restore

```bash
# Restore workspace
cp -r workspace/* ~/.openclaw/workspace/

# Restore memory
cp -r memory/* ~/.openclaw/memory/

# Restore cron
cp cron/jobs.json ~/.openclaw/cron/

# Config - manually add your API keys
```

## Last Updated
EOF
echo "" >> "$BACKUP_DIR/README.md"
echo "**$DATE $TIME**" >> "$BACKUP_DIR/README.md"

echo ""
echo "✅ Backup complete!"
echo "   Location: $BACKUP_DIR"
echo ""

# 7. Git sync
echo "📤 Syncing to Git..."
cd "$BACKUP_DIR"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "   Initializing git repo..."
    git init
    git branch -M main
    
    # Create .gitignore
    cat > .gitignore << 'GITIGNORE'
*.key
*.pem
.env
*.log
__pycache__/
*.pyc
node_modules/
.DS_Store
GITIGNORE
    
    echo ""
    echo "⚠️  Git initialized but no remote set!"
    echo "   Run: cd $BACKUP_DIR && git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git"
    exit 0
fi

# Check if remote exists
if ! git remote get-url origin &>/dev/null; then
    echo "⚠️  No git remote configured!"
    echo "   Run: cd $BACKUP_DIR && git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git"
    exit 0
fi

# Commit and push
git add -A
if git diff --staged --quiet; then
    echo "   No changes to commit"
else
    git commit -m "Auto backup - $DATE $TIME"
    
    # Push via SSH
    git push origin main --force 2>&1 && \
        echo "✅ Pushed to GitHub!" || \
        echo "⚠️  Push failed - check SSH key"
fi

echo ""
echo "🎉 Backup & sync complete!"
