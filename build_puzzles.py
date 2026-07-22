#!/usr/bin/env python3
"""
Compiles puzzles.csv (the answer key you edit) into puzzles.json (what the game reads).

Run this after editing puzzles.csv:
    python3 build_puzzles.py

Why a CSV: it's easy to bulk-edit dozens of rows in Excel/Google Sheets/Numbers
without hand-writing JSON syntax. Validates that every vehicleId/eraId/tripId
in the CSV actually exists in vehicles.json / trips.json, so a typo fails loudly
here instead of silently breaking the game for whoever's up next in the group chat.
"""
import csv
import json
import sys

def load(path):
    with open(path) as f:
        return json.load(f)

def main():
    vehicles = load('vehicles.json')
    trips = load('trips.json')
    vehicle_ids = {v['id']: v for v in vehicles}
    trip_ids = {t['id'] for t in trips}

    puzzles = []
    errors = []

    with open('puzzles.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vid = row['vehicleId'].strip()
            eid = row['eraId'].strip()
            tid = row['tripId'].strip()

            if vid not in vehicle_ids:
                errors.append(f"{row['date']}: unknown vehicleId '{vid}'")
                continue
            era_ids = {e['id'] for e in vehicle_ids[vid]['eras']}
            if eid not in era_ids:
                errors.append(f"{row['date']}: unknown eraId '{eid}' for vehicle '{vid}'")
                continue
            if tid not in trip_ids:
                errors.append(f"{row['date']}: unknown tripId '{tid}'")
                continue

            puzzles.append({
                "date": row['date'].strip(),
                "image": row['image'].strip(),
                "focusX": float(row['focusX']),
                "focusY": float(row['focusY']),
                "vehicleId": vid,
                "eraId": eid,
                "tripId": tid,
            })

    if errors:
        print("Found problems, fix these in puzzles.csv before publishing:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    with open('puzzles.json', 'w') as f:
        json.dump({"resetTimeZone": "America/Los_Angeles", "puzzles": puzzles}, f, indent=2)

    print(f"Wrote puzzles.json with {len(puzzles)} puzzles.")

if __name__ == '__main__':
    main()
