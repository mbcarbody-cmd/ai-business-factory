#!/usr/bin/env bash
set -euo pipefail

APP_NAME="parts-business-os"
APP_DIR="/opt/${APP_NAME}/fullstack"
SERVICE_NAME="parts-business-os.service"
HEALTH_URL="http://127.0.0.1:3060/health"
RELEASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

printf 'Deploying %s from %s\n' "$APP_NAME" "$RELEASE_DIR"

if [ "${EUID}" -ne 0 ]; then
  echo "Run deploy as root or through sudo."
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required. Install Node.js 20+ before deploy."
  exit 1
fi

mkdir -p "/opt/${APP_NAME}"
mkdir -p "/var/log/${APP_NAME}"

if ! id partsos >/dev/null 2>&1; then
  useradd --system --home "/opt/${APP_NAME}" --shell /usr/sbin/nologin partsos
fi

if [ -d "$APP_DIR" ]; then
  BACKUP_DIR="/opt/${APP_NAME}/backup-$(date +%Y%m%d-%H%M%S)"
  cp -a "$APP_DIR" "$BACKUP_DIR"
  echo "Previous release backed up to $BACKUP_DIR"
fi

mkdir -p "$APP_DIR"
rsync -a --delete \
  --exclude data/demo-db.json \
  --exclude node_modules \
  "$RELEASE_DIR/" "$APP_DIR/"

chown -R partsos:partsos "/opt/${APP_NAME}" "/var/log/${APP_NAME}"

cp "$APP_DIR/deploy/${SERVICE_NAME}" "/etc/systemd/system/${SERVICE_NAME}"
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

sleep 2

if ! curl -fsS "$HEALTH_URL" >/tmp/${APP_NAME}-health.json; then
  echo "Health check failed. Rolling back requires restoring the latest backup directory manually."
  systemctl status "$SERVICE_NAME" --no-pager || true
  exit 1
fi

echo "Health check passed:"
cat /tmp/${APP_NAME}-health.json

echo "Deploy complete."
