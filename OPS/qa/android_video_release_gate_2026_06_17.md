# Android Video Release Gate

Status: BLOCKED
Incident: #76

A release is not allowed from code review, deployment success or synthetic checks alone.

## Independent QA ownership

The implementer cannot approve the release. A separate QA owner must reproduce the critical path on the target device and attach evidence.

## Required device matrix

| Test | Android Chrome | Evidence required |
|---|---:|---|
| JPEG selection | pending | screenshot + filename/dimensions |
| PNG selection | pending | screenshot + filename/dimensions |
| WEBP selection | pending | screenshot + filename/dimensions |
| HEIC/HEIF conversion | pending | screenshot + conversion status |
| Multi-image preview | pending | preview screenshot |
| Built-in soundtrack | pending | audible playback confirmation |
| Uploaded audio | pending | audible playback confirmation |
| Video render | pending | non-empty file size |
| Playback | pending | player screenshot |
| Download/share | pending | downloaded/shared file proof |

## Hard rules

- Any failed critical row keeps the release blocked.
- Missing evidence equals FAIL.
- No user-facing claim of working, Android-ready, sell-ready or revenue-ready before PASS.
- No outreach, payment request or domain purchase before PASS.
- User-observed failures outrank staffing, documentation and marketing tasks.

## Current verdict

QA FAILED. Code changes exist, but real-device evidence does not yet exist.