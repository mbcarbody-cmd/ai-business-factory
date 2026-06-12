# Bugbot Review Rules

Bugbot should review this repo as an execution OS for revenue, delivery, QA, CFO, deploy and marketplace work.

## Always check

1. Does the change connect to a task in `OPS/task_board.json`?
2. Does the change update a proof path?
3. Are tests added or is there a clear no-test reason?
4. Does the change affect pricing, revenue or offer promises?
5. Does the change affect delivery scope or handoff?
6. Does the change affect deploy, health check or rollback?
7. Does the change affect marketplace data entities or workflow?
8. Does the change create security, privacy or data-loss risk?

## Blocking findings

Flag as blocking when:

- backend/API changes have no test or no no-test reason,
- data deletion or destructive command is introduced,
- pricing or offer copy changes without CFO/Judge note,
- production deploy path changes without rollback note,
- marketplace data model changes without migration/data impact note,
- secrets or env values are exposed,
- task board/proof path is missing for a significant change.

## Non-blocking findings

Flag as non-blocking when:

- docs can be clearer,
- naming is inconsistent,
- duplicate logic appears,
- TODO/FIXME exists without issue/task reference,
- output summary is missing.

## Preferred output

For every finding include:

- severity,
- file/path,
- why it matters,
- suggested fix,
- related OPS layer.
