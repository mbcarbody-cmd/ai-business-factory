# YouTube Transcript Intelligence Playbook

Date: 2026-06-15
Owner: Content Revenue Analyst + Data Policy Specialist
Status: active

## Purpose

Turn YouTube videos into revenue intelligence without waiting for the user to manually explain every video.

The goal is not to copy videos. The goal is to extract business signals:

- audience;
- pain;
- dream outcome;
- mechanism;
- offer;
- proof;
- acquisition channel;
- monetization;
- objections;
- next revenue action.

## Allowed inputs

1. User-provided transcript.
2. Creator-provided public captions where access is allowed.
3. Official API or permissioned source when available.
4. Short user-supplied clips or summaries.
5. Manual notes from watching the video.

## Guardrails

- No login bypass.
- No captcha bypass.
- No fake accounts.
- No private profile scraping.
- No bulk scraping.
- No full transcript republication.
- Store summaries, short snippets, timestamps and extracted signals, not copyrighted long-form text.
- Every row must include source_url, collected_at, method, allowed_use_note and confidence.

## Extraction hierarchy

1. Try existing captions/transcript from an allowed source.
2. If not available, record blocker and ask for user-provided transcript or manual notes when needed.
3. If the user owns or has permission for the media, audio transcription can be used.
4. If no transcript exists, extract from title, description, comments and public metadata only.

## Output template

For every video, produce:

- video_url;
- title;
- channel;
- transcript_status;
- source_method;
- audience;
- pain;
- mechanism;
- offer;
- CTA;
- monetization path;
- proof/examples;
- reusable hooks;
- revenue task;
- blocker;
- confidence.

## Apps Lab use

Every useful video must become one of:

- offer improvement;
- landing page hook;
- MVP idea;
- sales script;
- lead source;
- monetization test;
- stop/pivot lesson.

## Current priority

Use this pipeline for Apps Lab and Revenue Department first:

1. AI Date Planner.
2. AI Wingman.
3. NoSwipe curated intro experiment.
4. Other lightweight app experiments.
