# Automotive Parts CSV Cleanup — paid-service portfolio sample

**Demonstration, not paid client work. Synthetic demo OEM placeholders.**

A conservative data-cleaning helper for used-car-parts vendors, before eBay/marketplace import.

## Features
- Reads and normalizes vendor CSV (SKU, OEM, title, price, quantity)
- Detects duplicate SKUs, missing OEMs, multiple year mentions, unknown makes
- Splits *year and make mentioned* as clues, but explicitly leaves true fitment UNVERIFIED
- Generates a review queue, avoids formula injection in CSV cells
- Standard-library Python, no API keys and no external packages

## Run
```bash
python3 processor.py demo_input.csv cleaned.csv review.csv
```

## Proposed commercial packages
- EUR 90: 100-row pilot, cleaned CSV + review queue
- EUR 250–600: up to 1,000 rows (subject to actual data quality, fitment/photo scope, agreement)
- eBay native Seller Hub bulk template, MVL relationships and vehicle fitment research: separately scoped; **not implied by this demo**

**No buyer or earnings yet.** Example listings that prompted this sample:
- https://www.upwork.com/freelance-jobs/apply/eBay-Motors-CSV-Fitment-Specialist-Used-Rebuilt-Drivetrain-Parts_~022123421535036121301/
- https://www.upwork.com/freelance-jobs/apply/eBay-and-Online-Platform-Listing-Specialist_~022123592476587392010/

This portfolio proof is not a claim of eBay Seller Hub MVL production experience. Before accepting a contract, validate destination schema and a 10-20 row sample with the client.
