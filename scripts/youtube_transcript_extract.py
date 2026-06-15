#!/usr/bin/env python3
"""YouTube transcript helper for revenue intelligence.

This helper is intentionally conservative:
- no login or cookies;
- no captcha bypass;
- no bulk scraping;
- no video/audio download;
- output is metadata + transcript status + text if a permitted caption route works.

Preferred use: extract business signals, not republish full transcripts.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def video_id_from_url(url: str) -> str:
    patterns = [r"v=([A-Za-z0-9_-]{6,})", r"youtu\.be/([A-Za-z0-9_-]{6,})", r"shorts/([A-Za-z0-9_-]{6,})"]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url.strip()


def clean_vtt(text: str) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line:
            continue
        if re.fullmatch(r"\d+", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    deduped: list[str] = []
    previous = None
    for line in lines:
        if line != previous:
            deduped.append(line)
        previous = line
    return "\n".join(deduped)


def try_youtube_transcript_api(video_id: str, languages: list[str]) -> dict[str, Any] | None:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except Exception as exc:
        return {"ok": False, "method": "youtube_transcript_api", "error": f"dependency_missing: {exc}"}

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        text = "\n".join(item.get("text", "") for item in transcript if item.get("text"))
        return {"ok": True, "method": "youtube_transcript_api", "text": text, "segments": len(transcript)}
    except Exception as exc:
        return {"ok": False, "method": "youtube_transcript_api", "error": str(exc)}


def try_ytdlp_subtitles(url: str, languages: list[str]) -> dict[str, Any] | None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        out = str(tmp_path / "%(id)s.%(ext)s")
        lang_arg = ",".join(languages)
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            lang_arg,
            "--sub-format",
            "vtt",
            "-o",
            out,
            url,
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except FileNotFoundError:
            return {"ok": False, "method": "yt-dlp", "error": "dependency_missing: yt-dlp not installed"}
        except Exception as exc:
            return {"ok": False, "method": "yt-dlp", "error": str(exc)}

        if proc.returncode != 0:
            return {"ok": False, "method": "yt-dlp", "error": proc.stderr[-1000:]}

        files = list(tmp_path.glob("*.vtt"))
        if not files:
            return {"ok": False, "method": "yt-dlp", "error": "no_vtt_file_created"}

        text = clean_vtt(files[0].read_text(encoding="utf-8", errors="ignore"))
        return {"ok": True, "method": "yt-dlp_subtitles", "text": text, "file": files[0].name}


def make_result(url: str, languages: list[str]) -> dict[str, Any]:
    video_id = video_id_from_url(url)
    now = datetime.now(timezone.utc).isoformat()
    result: dict[str, Any] = {
        "video_url": url,
        "video_id": video_id,
        "collected_at": now,
        "languages_requested": languages,
        "allowed_use_note": "Use for internal business summary. Do not republish full transcript. No login, cookies, captcha bypass, or bulk scraping.",
        "status": "blocked",
        "method": None,
        "text": "",
        "error": None,
    }

    first = try_youtube_transcript_api(video_id, languages)
    if first and first.get("ok"):
        result.update({"status": "ok", "method": first.get("method"), "text": first.get("text", "")})
        return result

    second = try_ytdlp_subtitles(url, languages)
    if second and second.get("ok"):
        result.update({"status": "ok", "method": second.get("method"), "text": second.get("text", "")})
        return result

    result["error"] = {"youtube_transcript_api": first, "yt_dlp": second}
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="YouTube URL or video id")
    parser.add_argument("--langs", default="lt,en", help="Comma-separated language preference list")
    parser.add_argument("--out", default="", help="Optional output json path")
    args = parser.parse_args()

    languages = [lang.strip() for lang in args.langs.split(",") if lang.strip()]
    result = make_result(args.url, languages)
    payload = json.dumps(result, ensure_ascii=False, indent=2)

    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    return 0 if result.get("status") == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
