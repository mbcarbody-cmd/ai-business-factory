# Server shutdown backup and local move

Goal: preserve all repo knowledge before VPS shutdown and make the factory runnable from a Windows PC without paying for a server.

## What is already safe

This repository is on GitHub and remains the main source of truth after VPS shutdown.

Important current product files:

- `website/video-maker.html` — current P0 product
- `website/android.html` — Android/PWA wrapper
- `website/video-maker-android-qa.html` — Android Chrome WEBM proof harness
- `website/quick-video-qa-proof-intake.html` — QA proof intake before payment/outreach
- `website/manifest.webmanifest` — install metadata
- `website/sw.js` — offline app shell
- `OPS/product_gates/` — product decisions and revenue gates
- `OPS/qa/` — QA verdicts and proof
- `scripts/` — OPS audit and validation tools

## What may still be lost if it only exists on VPS

These must be copied manually from the VPS before the provider turns it off:

- `.env` files and non-public configuration
- local databases: `*.sqlite`, `*.db`, `*.dump`, `*.sql`
- uploaded files, generated videos, screenshots, logs and QA proof JSON
- cron/systemd service files
- nginx/apache config
- anything under `/var/www`, `/opt`, `/srv`, `/home/*/app`, `/home/*/ai-business-factory`

Do not commit real secrets into GitHub. Store them in a local encrypted archive or password manager.

## Emergency VPS backup command

Run this on the VPS while it is still online:

```bash
mkdir -p ~/server-backup
cd ~

# code and app folders
for d in ai-business-factory ai-tools-factory-os app apps www; do
  [ -d "$d" ] && tar -czf "server-backup/${d}.tar.gz" "$d"
done

# common deploy folders
sudo tar -czf ~/server-backup/var-www.tar.gz /var/www 2>/dev/null || true
sudo tar -czf ~/server-backup/opt.tar.gz /opt 2>/dev/null || true
sudo tar -czf ~/server-backup/srv.tar.gz /srv 2>/dev/null || true

# configs
sudo tar -czf ~/server-backup/etc-nginx.tar.gz /etc/nginx 2>/dev/null || true
sudo tar -czf ~/server-backup/systemd-services.tar.gz /etc/systemd/system 2>/dev/null || true

# databases and env files, copy as private local backup only
find ~ /var/www /opt /srv -type f \
  \( -name '.env' -o -name '*.sqlite' -o -name '*.db' -o -name '*.sql' -o -name '*.dump' -o -name '*proof*.json' \) \
  2>/dev/null | tar -czf ~/server-backup/private-env-db-proof-files.tar.gz -T -

sha256sum ~/server-backup/*.tar.gz > ~/server-backup/SHA256SUMS.txt
```

Then download to Windows:

```powershell
mkdir C:\AI_BACKUPS
scp -r user@SERVER_IP:~/server-backup C:\AI_BACKUPS\server-backup
```

## Local Windows restore from GitHub

Use `scripts/windows_backup_from_github.ps1` first. It clones/mirrors the repository into `C:\AI_FACTORY_BACKUP`.

Then use `scripts/windows_run_local.ps1` to run the browser product from the PC.

## Rule after shutdown

No paid VPS until one product passes its real-life functional gate and is worth using daily.

Priority is not demo pages. Priority is a finished tool that either saves work every day or can be sold.
