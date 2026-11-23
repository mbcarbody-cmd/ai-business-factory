#!/usr/bin/env python3
"""Conservative automotive parts catalog normalizer and review queue.
Does not infer verified vehicle compatibility or manufacture OEM matches.
"""
import csv
import re
import sys
from collections import Counter

MAKES = {
    "mercedes-benz": "Mercedes-Benz",
    "mercedes": "Mercedes-Benz",
    "volkswagen": "Volkswagen",
    "vw": "Volkswagen",
    "bmw": "BMW",
    "audi": "Audi",
    "toyota": "Toyota",
    "volvo": "Volvo",
    "hyundai": "Hyundai",
    "kia": "Kia",
    "lexus": "Lexus",
    "ford": "Ford",
    "opel": "Opel",
    "peugeot": "Peugeot",
    "renault": "Renault",
    "citroen": "Citroen",
}
YEAR_RE = re.compile(r"\b(?:19[89]\d|20[0-3]\d)\b")
OEM_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 .\\-/]{2,39}$")
FIELDS = [
    "vendor","sku","oem","title_clean","year_mentioned","make_mentioned",
    "model_unverified","quantity","price_eur","compatibility_status","review_flags",
]

def safe_cell(s):
    s = str(s or "").strip()
    return "'" + s if s.startswith(("=", "+", "-", "@", "\t", "\r")) else s

def make_from_title(title):
    t = title.lower()
    for token, canonical in sorted(MAKES.items(), key=lambda kv:-len(kv[0])):
        if re.search(r"(?<!\w)" + re.escape(token) + r"(?!\w)", t):
            return canonical
    return ""

def convert(row, sku_counts):
    title = " ".join((row.get("title") or "").split())
    sku = (row.get("sku") or "").strip().upper()
    oem = re.sub(r"\s+", "", (row.get("oem") or "").upper())
    years = YEAR_RE.findall(title)
    year = years[0] if years and len(set(years)) == 1 else ""
    make = make_from_title(title)
    issues = []
    if not sku: issues.append("missing_sku")
    elif sku_counts[sku] > 1: issues.append("duplicate_sku")
    if not oem: issues.append("missing_oem")
    elif not OEM_RE.fullmatch(oem): issues.append("oem_format_review")
    if len(set(years)) > 1: issues.append("multiple_years_check_fitment")
    if not make: issues.append("make_not_detected")
    if not title: issues.append("missing_title")
    try:
        quantity = int(row.get("quantity") or 0)
        if quantity < 0: raise ValueError
    except ValueError:
        quantity = 0
        issues.append("quantity_invalid")
    try:
        price = float((row.get("price_eur") or "0").replace(",", "."))
        if price < 0: raise ValueError
    except ValueError:
        price = 0.0
        issues.append("price_invalid")
    issues.append("fitment_requires_authoritative_check")
    return {
        "vendor":safe_cell(row.get("vendor")),"sku":safe_cell(sku),
        "oem":safe_cell(oem),"title_clean":safe_cell(title),
        "year_mentioned":year,"make_mentioned":make,"model_unverified":"",
        "quantity":quantity,"price_eur":f"{price:.2f}",
        "compatibility_status":"UNVERIFIED","review_flags":"; ".join(issues),
    }

def main():
    if len(sys.argv) != 4:
        raise SystemExit("python3 processor.py vendor.csv cleaned.csv review.csv")
    source, cleaned, review = sys.argv[1:]
    with open(source, encoding="utf-8-sig",newline="") as f:
        reader = csv.DictReader(f)
        needed = {"vendor","sku","oem","title","quantity","price_eur"}
        if not needed.issubset(set(reader.fieldnames or [])):
            raise ValueError("Input missing required columns: "+",".join(sorted(needed-set(reader.fieldnames or []))))
        raw = list(reader)
    counts = Counter((row.get("sku") or "").strip().upper() for row in raw)
    converted = [convert(row,counts) for row in raw]
    for path, records in ((cleaned,converted),(review,[r for r in converted if r["review_flags"]])):
        with open(path,"w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(records)
    print(f"Processed {len(converted)} rows; compatibility requires human/OEM validation.")

if __name__=="__main__":
    main()
