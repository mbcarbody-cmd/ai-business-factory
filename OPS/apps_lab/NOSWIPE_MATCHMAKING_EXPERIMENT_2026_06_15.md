# NoSwipe Matchmaking Experiment

Date: 2026-06-15
Owner: Apps Lab GM + Product Marketing + Customer Discovery
Status: active

## Decision

The dating idea starts as a matchmaking experiment, not as a full dating app.

## Core hypothesis

People who are tired of swiping may prefer one curated intro or one real-world activity suggestion over endless profile browsing.

## First proof target

Create 10 good intro attempts before any platform build.

A good intro means:

- both people opted in;
- both match on city, age range, intent and at least one real interest;
- the intro has a concrete low-pressure activity suggestion;
- both can give feedback after the intro.

## Intake form fields

- city;
- age range;
- dating intent;
- preferred pace;
- interests;
- dealbreakers;
- preferred meeting type;
- free days/times;
- safety preference;
- contact method;
- consent checkbox.

## Match review checklist

- same city or reachable distance;
- compatible intent;
- no obvious dealbreaker conflict;
- at least one shared interest;
- activity suggestion exists;
- both opted in;
- no automated bulk messages.

## Output for each intro

- intro id;
- person A profile summary;
- person B profile summary;
- match reason;
- suggested activity;
- suggested opener;
- feedback status;
- continue / stop decision.

## Data rule

Only user-submitted data and public activity/event sources may be used. No private profile scraping.

## Stop rule

If 10 intro attempts do not produce useful feedback or willingness to continue, do not build a dating app. Pivot to AI Date Planner or AI Wingman.
