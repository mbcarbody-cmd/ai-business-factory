# Parts Workforce OS Fullstack MVP

Used auto parts workforce and task tracking system.

## Features

- employee shift start and stop
- worker roles
- part ID creation
- OEM, vehicle, VIN, category, side, condition and shelf fields
- task tracking by worker and part ID
- task minutes and notes
- part status updates from task workflow
- photo workflow checklist
- image upload stored locally
- printable part labels
- dashboard by worker and status
- CSV export for tasks
- CSV export for parts
- simple JSON database

## Run locally

```bash
node server.js
```

Open:

```text
http://localhost:8110
```

## Run on server

```bash
cd products/parts-workforce-os/fullstack
PORT=8110 node server.js
```

## Data

Data is stored in:

```text
data/db.json
data/photos/
```

## Pilot scope

This is a working MVP for one warehouse or one used parts operation. It can be extended into login users, barcode scanner mode, RRR import/export, cloud photo storage and role permissions.
