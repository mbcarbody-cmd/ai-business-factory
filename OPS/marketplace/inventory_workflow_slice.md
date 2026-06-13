# Inventory Workflow Slice

Date: 2026-06-13
Owner: MARKET-2 Warehouse Autonomy Director
Status: proof slice

## Goal

Create the smallest useful workflow for one item:

1. item intake;
2. location suggestion;
3. quality note;
4. listing text draft;
5. state tracking.

## Required item fields

- item name
- item code
- vehicle or source model
- side or position
- condition
- size class
- category
- photo count

## Sample flow

Input: medium-size door electronics item with five photos.

System output:

- suggested zone: A-02
- suggested shelf: 03
- suggested box: M
- quality note: used tested
- text draft status: ready for review
- next action: review photos and publish

## States

- new
- located
- draft ready
- published
- reserved
- completed
- aged review

## Done proof

This workflow is useful when one item can move from intake to suggested location and text draft without manual guessing.
