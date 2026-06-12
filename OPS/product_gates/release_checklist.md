# Release / Sell-Ready Checklist

Owner: JUDGE-1 Release Gate Judge

A product cannot move to the next stage unless every required item is checked or explicitly waived by the judge with reason.

## Idea -> Validated problem

- Buyer is named.
- Pain is concrete.
- Buyer can pay.
- Competitor or alternative exists.
- Value proposition is one sentence.

## Validated problem -> Build ready

- Scope is clear.
- Expected output is clear.
- Data/input requirements are known.
- Owner is assigned.
- Build task exists in `OPS/task_board.json`.

## Build ready -> Demo ready

- Demo can be opened or shown.
- Main workflow works end-to-end.
- No critical missing screen/document.
- Demo has a user story.

## Demo ready -> QA ready

- QA checklist exists.
- Main failure modes listed.
- Known bugs entered in `OPS/qa/bug_board.json`.

## QA ready -> Deploy ready

- Test or smoke test completed.
- Deploy path documented.
- Health check documented.
- Rollback note documented.

## Deploy ready -> Sell ready

- Offer pack exists.
- Price and margin checked by CFO layer.
- Landing/sales path exists.
- Outreach segment selected.
- No dangerous or exaggerated claims.

## Sell ready -> Delivery ready

- Intake form exists.
- Delivery SOP exists.
- Handoff text exists.
- Support/maintenance next step exists.

## Judge veto rules

Release is blocked if:

- no test,
- no sales path,
- no price logic,
- no delivery handoff,
- no rollback path,
- critical bug exists,
- product promise is bigger than actual delivery.
