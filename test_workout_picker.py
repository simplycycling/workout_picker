import unittest
import sqlite3
import os
from workout_picker import (
    setup_database,
    select_kb,
    select_core,
    display_counts,
    clear_database,
    kb,
    core,
)


class TestWorkoutPicker(unittest.TestCase):
    def setUp(self):
        """Set up a test database before each test."""
        self.test_db = "test_selection_counts.db"
        self.conn = setup_database(self.test_db)
        self.conn.close()

    def tearDown(self):
        """Clean up the test database after each test."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_setup_database(self):
        """Test that the database is created with correct tables and initial data."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()

        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        self.assertIn(("kb_counts",), tables)
        self.assertIn(("core_counts",), tables)

        # Check if all KB items are initialized
        cursor.execute("SELECT item FROM kb_counts")
        kb_items = {row[0] for row in cursor.fetchall()}
        self.assertEqual(set(kb), kb_items)

        # Check if all Core items are initialized
        cursor.execute("SELECT item FROM core_counts")
        core_items = {row[0] for row in cursor.fetchall()}
        self.assertEqual(set(core), core_items)

        # Check if all counts are initialized to 0
        cursor.execute("SELECT count FROM kb_counts")
        kb_counts = {row[0] for row in cursor.fetchall()}
        self.assertTrue(all(count == 0 for count in kb_counts))

        conn.close()

    def test_select_kb(self):
        """Test that KB selection works and increments count."""
        conn = sqlite3.connect(self.test_db)
        
        # Test selection is from valid options
        selected = select_kb(conn)
        self.assertIn(selected, kb)

        # Test count was incremented
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM kb_counts WHERE item = ?", (selected,))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

        conn.close()

    def test_select_core(self):
        """Test that Core selection works and increments count."""
        conn = sqlite3.connect(self.test_db)
        
        # Test selection is from valid options
        selected = select_core(conn)
        self.assertIn(selected, core)

        # Test count was incremented
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM core_counts WHERE item = ?", (selected,))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

        conn.close()

    def test_clear_database(self):
        """Test that clear_database resets all counts to 0."""
        conn = sqlite3.connect(self.test_db)
        
        # First increment some counts
        cursor = conn.cursor()
        cursor.execute("UPDATE kb_counts SET count = 1 WHERE item = ?", (kb[0],))
        cursor.execute("UPDATE core_counts SET count = 1 WHERE item = ?", (core[0],))
        conn.commit()

        # Clear the database
        clear_database(conn)

        # Verify all counts are 0
        cursor.execute("SELECT count FROM kb_counts")
        kb_counts = {row[0] for row in cursor.fetchall()}
        self.assertTrue(all(count == 0 for count in kb_counts))

        cursor.execute("SELECT count FROM core_counts")
        core_counts = {row[0] for row in cursor.fetchall()}
        self.assertTrue(all(count == 0 for count in core_counts))

        conn.close()

    def test_display_counts(self):
        """Test that display_counts shows correct information."""
        conn = sqlite3.connect(self.test_db)
        
        # Set up some test data
        cursor = conn.cursor()
        cursor.execute("UPDATE kb_counts SET count = 2 WHERE item = ?", (kb[0],))
        cursor.execute("UPDATE core_counts SET count = 1 WHERE item = ?", (core[0],))
        conn.commit()

        # Note: display_counts is primarily for output, so we can't easily test its output
        # but we can verify it doesn't raise any exceptions
        try:
            display_counts(conn)
        except Exception as e:
            self.fail(f"display_counts raised an exception: {e}")

        conn.close()


if __name__ == "__main__":
    unittest.main() 