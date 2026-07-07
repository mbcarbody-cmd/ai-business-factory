# Agent memory: product reality and next actions

This file exists so future agents do not lose context after VPS shutdown.

## Owner decision

The VPS is not worth paying for while there is no working revenue product. Preserve knowledge, move development to Windows/local, and only rent a server again after a real product passes a functional gate.

## Reality check

Do not present demo pages as finished products. Half-working buttons or fake flows are not acceptable.

A product is real only when:

1. the main user action works end-to-end;
2. the output is a real artifact or real saved value;
3. it works on the target device, not only desktop theory;
4. it can be used without developer handholding;
5. QA proof exists.

## Current P0

Current P0 in this repo is `Quick Product Video`:

- local photo upload;
- vertical product video rendering;
- WEBM recording;
- playback;
- download;
- Android Chrome/PWA proof.

Primary files:

- `website/video-maker.html`
- `website/android.html`
- `website/video-maker-android-qa.html`
- `website/quick-video-qa-proof-intake.html`

## Blocked from sales

No outreach, no payment request, no paid-pilot claim until Android Chrome test proves:

- photos load;
- preview renders;
- non-empty WEBM is generated;
- video plays;
- file downloads.

## User complaint to remember

The owner is unhappy because too much effort went into architecture, agents, security, KPIs and demos, while usable products were not delivered. Future work must ship usable local tools first.

Specifically mentioned missing product: motorcycle ride recording app. If resumed, define it as a real MVP:

- Android phone records ride video or at least GPS track;
- saves route file locally;
- shows distance/time/speed;
- exports/shareable file;
- works before any backend/server.

## Next actions after local move

1. Run local Windows backup.
2. Run `website/video-maker.html` locally.
3. Test it on Android Chrome via local network or GitHub Pages.
4. Save proof JSON/screenshots/video result.
5. Fix only blocking product bugs.
6. Do not build new dashboard/agent layers until P0 works.
