#!/bin/bash
# Just sync existing backup to Git (no new backup)

BACKUP_DIR="$HOME/.openclaw/backup"

if [ ! -d "$BACKUP_DIR/.git" ]; then
    echo "❌ No git repo at $BACKUP_DIR"
    echo "   Run backup_and_sync.sh first"
    exit 1
fi

cd "$BACKUP_DIR"

echo "📤 Syncing to Git..."

git add -A
if git diff --staged --quiet; then
    echo "✅ No changes to sync"
    exit 0
fi

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)

git commit -m "Sync - $DATE $TIME"

git push origin main --force 2>&1 && \
    echo "✅ Pushed to GitHub!" || \
    echo "⚠️  Push failed - check SSH key"
