# Parts Seller OS Build Contract

Date: 2026-06-15
Owner: Solution Architect
Status: active

Goal: build a local one-seller workflow before expansion.

Required local flow:

1. Add sample item.
2. Suggest category.
3. Suggest location.
4. Calculate suggested value and floor.
5. Mark listing state.
6. Create export row.
7. Reserve item.
8. Move exceptions to review queue.

Inputs:

- sample data
- category rules
- location rules
- value rules
- listing state rules

Done proof:

A sample item can move through the full flow locally.

Block rule:

No expansion before local flow works.
