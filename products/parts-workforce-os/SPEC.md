# Parts Workforce OS

## Purpose

A workforce time and task tracking system for used parts operations.

The system tracks who did what, when, on which part ID, and what the current status of the part is.

## Core workflow

1. Vehicle or part batch received.
2. Part is created with internal part ID.
3. Worker starts a task.
4. Worker selects task type.
5. Worker scans or enters part ID.
6. Worker adds quantity, notes and photos.
7. System records start time, end time and duration.
8. System updates the part status.
9. Manager sees daily productivity and bottlenecks.
10. Labels are generated for storage and marketplace use.

## Task types

- received part
- dismantled part
- cleaned part
- photographed part
- photo edited
- listing prepared
- price checked
- quality checked
- label printed
- stored in shelf
- packed
- shipped
- returned
- defect found

## Part data

- internal part ID
- OEM number
- vehicle model
- donor vehicle VIN
- category
- side
- condition
- shelf location
- photos
- worker history
- current status
- marketplace listing status

## Employee data

- worker name
- role
- shift start
- shift end
- task count
- total task time
- average time per task
- errors or returns linked to worker tasks

## Manager dashboard

- daily worker hours
- tasks by worker
- parts created today
- photos uploaded today
- labels printed today
- parts ready for listing
- parts blocked by missing data
- slowest workflow step

## MVP modules

- worker time clock
- task entry screen
- part ID generator
- label generator
- photo upload and basic edit checklist
- daily productivity dashboard
- CSV export

## First sellable pilot

A simple browser-based MVP for one used parts company.

Pilot scope:
- up to 5 workers
- task tracking
- part ID tracking
- CSV export
- printable labels
- simple dashboard

Pilot delivery target: 72 hours.
