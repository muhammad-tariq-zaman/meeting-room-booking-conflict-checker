import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import conflicts

def row(booking_id, room, date, start, end, booked_by):
    return {"booking_id": booking_id, "room": room, "date": date,
            "start": start, "end": end, "booked_by": booked_by}

class TestBookingConflictChecker(unittest.TestCase):
    def test_overlap_detected(self):
        found, _ = conflicts([row("B-1", "Room A", "2026-11-11", "09:00", "10:00", "Ali"),
                              row("B-2", "Room A", "2026-11-11", "09:30", "10:30", "Sara")])
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0][0][0], "B-1")

    def test_back_to_back_no_conflict(self):
        found, _ = conflicts([row("B-1", "Room A", "2026-11-11", "09:00", "10:00", "Ali"),
                              row("B-2", "Room A", "2026-11-11", "10:00", "11:00", "Sara")])
        self.assertEqual(found, [])

    def test_different_rooms_no_conflict(self):
        found, _ = conflicts([row("B-1", "Room A", "2026-11-11", "09:00", "10:00", "Ali"),
                              row("B-2", "Room B", "2026-11-11", "09:00", "10:00", "Sara")])
        self.assertEqual(found, [])

    def test_different_dates_no_conflict(self):
        found, _ = conflicts([row("B-1", "Room A", "2026-11-11", "09:00", "10:00", "Ali"),
                              row("B-2", "Room A", "2026-11-12", "09:00", "10:00", "Sara")])
        self.assertEqual(found, [])

    def test_contained_booking_conflicts(self):
        found, _ = conflicts([row("B-1", "Room A", "2026-11-11", "09:00", "12:00", "Ali"),
                              row("B-2", "Room A", "2026-11-11", "10:00", "11:00", "Sara")])
        self.assertEqual(len(found), 1)

    def test_pair_listed_once(self):
        found, total = conflicts([row("B-1", "Room A", "2026-11-11", "09:00", "10:00", "Ali"),
                                  row("B-2", "Room A", "2026-11-11", "09:30", "10:30", "Sara")])
        self.assertEqual((len(found), total), (1, 2))

    def test_sorted_by_room_then_time(self):
        found, _ = conflicts([row("B-3", "Room B", "2026-11-11", "09:00", "10:00", "Bob"),
                              row("B-4", "Room B", "2026-11-11", "09:30", "10:30", "Sara"),
                              row("B-1", "Room A", "2026-11-11", "09:00", "10:00", "Ali"),
                              row("B-2", "Room A", "2026-11-11", "09:30", "10:30", "Sara")])
        self.assertEqual(found[0][0][1], "Room A")

    def test_empty_input(self):
        self.assertEqual(conflicts([]), ([], 0))
