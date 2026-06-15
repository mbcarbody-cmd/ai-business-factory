# Parts Seller OS Eval Plan

Date: 2026-06-15
Owner: Evaluation Engineer
Status: active

## Goal

Check whether the local prototype makes useful decisions before any expansion.

## Required checks

1. Category suggestion is not empty.
2. Location suggestion is not empty.
3. Value and floor are numeric.
4. Floor is below suggested value.
5. Listing state is one of ready, needs_photo, needs_review.
6. Ready item can be reserved.
7. Blocked item cannot be reserved.
8. Export row includes item, title, code, category, location, value and state.

## Pass condition

Both sample items produce valid export rows and correct reserve state.

## Next action

Convert these checks into automated local tests after prototype stabilizes.
