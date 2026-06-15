# YouTube Transcript Runbook

Date: 2026-06-15
Owner: Content Revenue Analyst
Status: active

## Install optional tools

```bash
python -m pip install youtube-transcript-api yt-dlp
```

## Extract transcript/captions status

```bash
python scripts/youtube_transcript_extract.py "https://www.youtube.com/watch?v=VIDEO_ID" --langs lt,en --out OPS/content_intelligence/tmp_video_result.json
```

## Revenue deconstruction after transcript exists

Convert text into:

- audience;
- pain;
- mechanism;
- offer;
- proof;
- CTA;
- monetization;
- objections;
- next revenue action.

## Blocker handling

If the tool cannot access captions, do not mark the video as analyzed. Record blocker in:

- `OPS/content_intelligence/youtube_video_intake_queue_2026_06_15.json`
- `OPS/revenue_department/video_revenue_deconstruction_queue_2026_06_15.json`

Then continue with the next revenue action instead of waiting.

## Compliance notes

- No cookies.
- No login bypass.
- No captcha bypass.
- No bulk scraping.
- No full transcript republication.
- Use short snippets and summaries for internal revenue intelligence.
