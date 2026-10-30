import json
import pathlib
import tempfile
import unittest

from midtermQuiz import CATEGORIES, DEFAULT_STATUS, STATUSES, TaskStore


class TaskStoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self._tmp.name) / "tasks.json"
        self.store = TaskStore(self.path)

    def tearDown(self):
        self._tmp.cleanup()

    def test_missing_file_starts_empty(self):
        self.assertEqual(self.store.rows(), [])

    def test_add_defaults_to_in_progress(self):
        task = self.store.add("Review notes", "Study")
        self.assertEqual(task["status"], DEFAULT_STATUS)

    def test_add_strips_whitespace(self):
        task = self.store.add("  Review notes  ", "Study")
        self.assertEqual(task["title"], "Review notes")

    def test_add_rejects_empty_title(self):
        self.assertIsNone(self.store.add("   ", "Study"))
        self.assertEqual(self.store.rows(), [])
        self.assertFalse(self.path.exists())

    def test_add_rejects_unknown_category(self):
        self.assertIsNone(self.store.add("Review notes", "Work"))
        self.assertEqual(self.store.rows(), [])

    def test_add_accepts_every_category(self):
        for category in CATEGORIES:
            self.assertIsNotNone(self.store.add(f"Task {category}", category))

    def test_saves_and_reloads(self):
        self.store.add("Review notes", "Study")
        self.store.add("Team dinner", "Personal Event")

        reloaded = TaskStore(self.path)
        self.assertEqual(
            [t["title"] for t in reloaded.rows()],
            ["Review notes", "Team dinner"],
        )

    def test_saved_file_is_valid_json(self):
        self.store.add("Review notes", "Study")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(
            data, [{"title": "Review notes", "category": "Study", "status": "In Progress"}]
        )

    def test_update_changes_only_given_field(self):
        self.store.add("Review notes", "Study")
        self.store.update(0, status="Completed")

        task = self.store.rows()[0]
        self.assertEqual(task["status"], "Completed")
        self.assertEqual(task["title"], "Review notes")
        self.assertEqual(task["category"], "Study")

    def test_update_rejects_bad_values(self):
        self.store.add("Review notes", "Study")

        self.assertIsNone(self.store.update(0, status="Done"))
        self.assertIsNone(self.store.update(0, title="   "))
        self.assertIsNone(self.store.update(0, category="Work"))
        self.assertIsNone(self.store.update(9, status="Completed"))
        self.assertIsNone(self.store.update(-1, status="Completed"))
        self.assertIsNone(self.store.update("0", status="Completed"))
        self.assertEqual(self.store.rows()[0]["title"], "Review notes")

    def test_update_accepts_every_status(self):
        self.store.add("Review notes", "Study")
        for status in STATUSES:
            self.assertIsNotNone(self.store.update(0, status=status))

    def test_update_persists(self):
        self.store.add("Review notes", "Study")
        self.store.update(0, title="Review notes v2")

        self.assertEqual(TaskStore(self.path).rows()[0]["title"], "Review notes v2")

    def test_update_with_same_values_does_not_rewrite_file(self):
        self.store.add("Review notes", "Study")
        before = self.path.stat().st_mtime_ns

        self.store.update(0, title="Review notes", category="Study", status="In Progress")

        self.assertEqual(self.path.stat().st_mtime_ns, before)
        self.assertEqual(self.store.rows()[0]["title"], "Review notes")

    def test_update_with_one_real_change_rewrites_file(self):
        self.store.add("Review notes", "Study")
        before = self.path.stat().st_mtime_ns

        self.store.update(0, category="Study", status="Completed")

        self.assertNotEqual(self.path.stat().st_mtime_ns, before)
        self.assertEqual(TaskStore(self.path).rows()[0]["status"], "Completed")

    def test_delete_removes_by_index(self):
        self.store.add("Review notes", "Study")
        self.store.add("Team dinner", "Personal Event")

        removed = self.store.delete(0)
        self.assertEqual(removed["title"], "Review notes")
        self.assertEqual([t["title"] for t in self.store.rows()], ["Team dinner"])

    def test_delete_rejects_bad_index(self):
        self.store.add("Review notes", "Study")
        self.assertIsNone(self.store.delete(5))
        self.assertEqual(len(self.store.rows()), 1)

    def test_duplicate_titles_delete_independently(self):
        self.store.add("Task", "Study")
        self.store.add("Task", "School")
        self.store.delete(0)

        self.assertEqual(self.store.rows()[0]["category"], "School")

    def test_progress_counts_completed(self):
        for i in range(5):
            self.store.add(f"Task {i}", "Study")
        for i in range(3):
            self.store.update(i, status="Completed")

        self.assertEqual(self.store.progress(), (3, 5, 60))
        self.assertEqual(self.store.progress_text(), "3/5 completed (60%)")

    def test_progress_on_empty_store(self):
        self.assertEqual(self.store.progress(), (0, 0, 0))
        self.assertEqual(self.store.progress_text(), "0/0 completed (0%)")

    def test_save_leaves_no_temp_file(self):
        self.store.add("Review notes", "Study")
        self.assertFalse(self.path.with_name(self.path.name + ".tmp").exists())
        self.assertTrue(self.path.exists())

    def test_empty_file_starts_empty_without_quarantine(self):
        self.path.write_text("", encoding="utf-8")
        store = TaskStore(self.path)

        self.assertEqual(store.rows(), [])
        self.assertFalse(self.path.with_name(self.path.name + ".corrupt").exists())

    def test_whitespace_only_file_starts_empty_without_quarantine(self):
        self.path.write_text("  \n\t\n ", encoding="utf-8")
        store = TaskStore(self.path)

        self.assertEqual(store.rows(), [])
        self.assertFalse(self.path.with_name(self.path.name + ".corrupt").exists())

    def test_corrupt_file_starts_empty_and_keeps_original(self):
        self.path.write_text("{not json", encoding="utf-8")
        store = TaskStore(self.path)

        self.assertEqual(store.rows(), [])
        self.assertTrue(self.path.with_name(self.path.name + ".corrupt").exists())

    def test_non_list_file_starts_empty(self):
        self.path.write_text('{"title": "x"}', encoding="utf-8")
        store = TaskStore(self.path)

        self.assertEqual(store.rows(), [])

    def test_non_dict_entries_are_dropped(self):
        self.path.write_text('["nope", {"title": "ok", "category": "Study", "status": "In Progress"}]', encoding="utf-8")
        store = TaskStore(self.path)

        self.assertEqual([t["title"] for t in store.rows()], ["ok"])


if __name__ == "__main__":
    unittest.main()
