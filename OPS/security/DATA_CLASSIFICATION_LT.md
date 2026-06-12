# Data Classification LT

Date: 2026-06-12
Owner: CISO / Security Judge
Purpose: apibrezti kokius duomenis galima rodyti viesai, ka laikyti viduje, ka saugoti kaip confidential ir kas yra restricted.

## Public

Galima rodyti viesai:
- public landing page text,
- public offer descriptions,
- public pricing ranges after CFO approval,
- public blog/content,
- public documentation without internal routes or secrets.

## Internal

Tik komandai / agentams:
- task board,
- architecture docs,
- product roadmap,
- QA bug board,
- delivery SOP,
- growth plans.

Controls:
- repo access only for required people/tools,
- no posting to public channels without review.

## Confidential

Ribotas naudojimas:
- lead pipeline,
- customer details,
- supplier lists,
- pricing logic,
- competitor intelligence,
- marketplace strategy,
- warehouse layout and inventory value.

Controls:
- mask before AI prompts when possible,
- no public screenshots,
- no public issues,
- no unrestricted exports.

## Restricted

Griezciausias lygis:
- API keys,
- tokens,
- passwords,
- private keys,
- cookies/sessions,
- database URLs,
- payment provider keys,
- production backups,
- service account files.

Controls:
- never commit,
- never paste in chat,
- never print in logs,
- store only in secrets manager/GitHub secrets,
- rotate immediately after exposure.

## AI prompt rules

Before sending data to any AI model ask:

1. Is this public, internal, confidential or restricted?
2. Can it be anonymized?
3. Is exact data needed?
4. Is there customer or supplier information?
5. Is there a secret or credential?
6. Is output going to be stored?

Restricted data never goes to prompts.

## Final rule

When unsure, classify one level higher and ask Security Judge before sharing.
