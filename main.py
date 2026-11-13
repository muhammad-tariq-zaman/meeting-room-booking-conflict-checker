"""Find overlapping meeting-room bookings in a bookings CSV.

Usage: python3 main.py bookings.csv
CSV columns: booking_id,room,date,start,end,booked_by.
start and end are HH:MM times on the same date. Two bookings
conflict when they are for the same room on the same date and
their time ranges overlap. Back-to-back bookings (one ends exactly
when the next starts) do NOT conflict. Each conflicting pair is
listed once.
"""
import argparse, csv, sys

def _minutes(value):
    hours, minutes = value.strip().split(":")
    return int(hours) * 60 + int(minutes)

def conflicts(rows):
    bookings = []
    for row in rows:
        bookings.append((row["booking_id"].strip(), row["room"].strip(),
                         row["date"].strip(), _minutes(row["start"]),
                         _minutes(row["end"]), row["start"].strip(),
                         row["end"].strip(), row["booked_by"].strip()))
    found = []
    for i in range(len(bookings)):
        for j in range(i + 1, len(bookings)):
            a = bookings[i]
            b = bookings[j]
            if a[1] != b[1] or a[2] != b[2]:
                continue
            if a[3] < b[4] and b[3] < a[4]:
                found.append((a, b))
    found.sort(key=lambda p: (p[0][1], p[0][2], p[0][3], p[1][0]))
    return found, len(bookings)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        found, total = conflicts(list(csv.DictReader(f)))
    for a, b in found:
        print(f"CONFLICT {a[1]} {a[2]}: {a[0]} ({a[5]}-{a[6]}, {a[7]}) overlaps {b[0]} ({b[5]}-{b[6]}, {b[7]})")
    print(f"{len(found)} conflict(s) across {total} booking(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
