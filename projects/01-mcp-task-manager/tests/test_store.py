import tempfile
import unittest
from pathlib import Path
from store import TaskStore


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "tasks.db"
        self.store = TaskStore(self.path)

    def tearDown(self):
        self.temp.cleanup()

    def test_persistence_and_status_filter(self):
        task = self.store.create("Renew Lambda certificate", "Synthetic example")
        self.store.update_status(task["id"], "done")
        reopened = TaskStore(self.path)
        self.assertEqual(reopened.search("lambda", "done")[0]["id"], task["id"])
        self.assertEqual(reopened.search(status="todo"), [])

    def test_search_is_literal_and_sql_safe(self):
        self.store.create("Investigate 100% CPU")
        self.store.create("Other task")
        self.assertEqual(len(self.store.search("%")), 1)
        self.assertEqual(self.store.search("' OR 1=1 --"), [])
        self.assertEqual(len(self.store.search()), 2)

    def test_bad_inputs_and_missing_task(self):
        for title in [" ", "x" * 201]:
            with self.assertRaises(ValueError):
                self.store.create(title)
        with self.assertRaises(ValueError):
            self.store.create("Valid", "x" * 10001)
        with self.assertRaises(ValueError):
            self.store.update_status(999, "done")
        with self.assertRaises(ValueError):
            self.store.search(status="invalid")
        for limit in [0, 101]:
            with self.assertRaises(ValueError):
                self.store.search(limit=limit)


if __name__ == "__main__":
    unittest.main()
