# Part Photo Upload Requirements

A final product must support heavy photo workflows. Some parts need only a few photos, but interior sets, body kits, engine sets, boat parts, aircraft components and large assemblies may require many images.

## Minimum requirement

Each part or part set must support at least 25 photos.

This is required for:

- interior sets
- seat sets
- door card sets
- dashboard sets
- body kits
- engine sets
- gearbox sets
- suspension sets
- boat parts
- motorcycle fairing sets
- aircraft and helicopter component sets
- damaged or defect-heavy parts

## Photo data model

Each photo must store:

- photo ID
- linked part ID
- linked donor asset ID where needed
- file path
- thumbnail path
- original file path
- sort order
- main photo flag
- angle / view type
- defect photo flag
- upload user
- upload timestamp
- edit timestamp
- AI quality status
- marketplace export status

## Photo workflow

Required actions:

- upload multiple photos at once
- drag and reorder photos
- select main photo
- rotate left
- rotate right
- crop
- angle adjustment
- delete photo
- mark as defect photo
- mark as hidden from marketplace
- view original
- generate thumbnails
- compress for web
- keep original for archive

## Performance requirement

Photo upload must not freeze the page.

Required:

- immediate upload progress
- background thumbnail generation
- background compression
- lazy loading thumbnails
- limit original file size
- warn if file is too large
- show failed upload state
- retry failed upload

## AI photo checks

AI should check:

- blurry photo
- dark photo
- duplicate photo
- missing main angle
- missing defect close-up
- poor background
- wrong part in photo
- photo count too low for category

## Category-based photo templates

The system should suggest required photo sets by category.

Example: simple part

- front
- back
- label / code
- defect close-up if needed

Example: interior set

- full set overview
- front seats
- rear seats
- door cards
- dashboard pieces if included
- airbags / belts if included
- damage close-ups
- labels and codes

Example: body panel

- outside
- inside
- mounting points
- paint code if visible
- damage close-ups

Example: boat / jet ski part

- full part
- connection points
- serial or casting number
- corrosion / damage close-ups

## Marketplace export rule

Not every internal photo must be exported to every marketplace.

Per photo, system needs:

- export to own shop
- export to marketplace channel A
- export to marketplace channel B
- internal only

## Release gate

Photo module is not complete until a user can upload 25 photos to one part, reorder them, choose main photo, edit basic rotation/crop, and the page still remains fast.
