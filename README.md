# meeting-room-booking-conflict-checker

Find overlapping meeting-room bookings from a CSV: two bookings conflict when they are for the same room on the same date and their time ranges overlap — back-to-back bookings (one ends exactly when the next starts) do not conflict, and each conflicting pair is listed once.

Sample input is included (sample.csv with four bookings).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
CONFLICT Room A 2026-11-11: B-1 (09:00-10:00, Ali) overlaps B-2 (09:30-10:30, Sara)
1 conflict(s) across 4 booking(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
