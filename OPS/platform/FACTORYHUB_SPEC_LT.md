# FactoryHub Spec LT

Date: 2026-06-13
Owner: CTO-1 Product Factory Architect + COO-1 Execution Architect
Status: platform direction

## Decision

Do not replace GitHub now. Build a focused control layer on top of GitHub.

GitHub remains:
- git history;
- file storage;
- commits;
- branches;
- basic review trail.

FactoryHub becomes:
- operating dashboard;
- agent task control;
- proof tracking;
- product gate control;
- artifact viewer;
- data quality ledger;
- delivery handoff system.

## Why not build full GitHub replacement now

Full git hosting is a large platform problem. It requires auth, permissions, diff viewer, branches, storage, review system, CI, security, billing and uptime. It would slow the current business factory.

The fastest useful path is to build the missing layer that GitHub does not give us:

- agent-friendly work control;
- proof-first task board;
- owner and blocker visibility;
- product maturity gates;
- business metrics;
- customer pipeline view;
- data provenance view;
- cockpit for decisions.

## FactoryHub MVP

### 1. Project cockpit

Shows:
- active lanes;
- owners;
- status;
- blocker;
- next action;
- output path;
- proof state.

### 2. Agent workbench

Shows every agent:
- role;
- current task;
- allowed tools;
- last output;
- next handoff;
- blocked reason.

### 3. Proof vault

Every artifact has:
- file path;
- owner;
- task id;
- created at;
- linked product;
- QA note;
- next action.

### 4. Product gate board

Every product has:
- stage;
- next gate;
- required proof;
- risk notes;
- release status.

### 5. Data ledger view

Every collected row has:
- source;
- timestamp;
- method;
- confidence;
- target use;
- review status.

### 6. Delivery board

Every package has:
- scope;
- intake;
- checklist;
- handoff;
- maintenance note.

## MVP architecture

Start simple:

- static frontend first;
- JSON files as database;
- GitHub repo as storage;
- local server for testing;
- later add backend and login.

Possible later stack:

- Next.js or simple React frontend;
- FastAPI or Node backend;
- Postgres database;
- GitHub API sync;
- background worker;
- role based permissions;
- audit log.

## First build slice

Build this before any full platform:

1. CEO Cockpit reads OPS JSON files.
2. Shows lanes, tasks, blockers and proof paths.
3. Shows product stages.
4. Shows data quality rows.
5. Shows artifact list.
6. Lets operator choose next best task.

## Rule

FactoryHub is not a code hosting product first. It is an AI business operating system first.

## Done proof

FactoryHub MVP is useful when:

- one page shows real OPS data;
- blocked work is visible;
- every active lane has next action;
- every done item has proof path;
- product gates are visible;
- data quality status is visible;
- next best action is visible.
