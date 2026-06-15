# Browser Agent Public Data Rules

Date: 2026-06-15
Owner: Data Policy Specialist + Apps Lab GM
Status: active

## Purpose

Browser agents support Apps Lab by collecting useful public information without private scraping, fake accounts or platform-rule bypass.

## Allowed public data

- public event pages;
- public venue pages;
- public business pages;
- public app landing pages;
- public competitor pricing pages;
- public blog/news/social posts that do not require login;
- public app store descriptions and reviews where allowed.

## Required row fields

- source_url;
- collected_at;
- source_type;
- topic;
- useful_signal;
- allowed_use_note;
- confidence;
- next_action.

## Blocked methods

- private profile scraping;
- fake accounts;
- login-wall bypass;
- captcha bypass;
- bulk messaging;
- copying protected content, catalogues or private photos.

## Apps Lab use cases

- dating fatigue research;
- local events and activities;
- date venue ideas;
- AI wingman competitor teardowns;
- micro app trend examples;
- landing page hooks and CTA patterns.

## Done rule

No research row is valid without source_url and allowed_use_note.
