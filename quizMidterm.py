import json
import pathlib

import tkinter as tk
from tkinter import messagebox, ttk

CATEGORIES = ("Study", "Personal Event", "School")
STATUSES = ("In Progress", "Completed")
DEFAULT_STATUS = "In Progress"
DATA_FILE = pathlib.Path(__file__).with_name("tasks.json")

def iAmFunction():
    print("HEllo World")

class TaskStore:
    def __init__(self, path=DATA_FILE):
        self.path = pathlib.Path(path)
        self.tasks = self._load()

    def _title_exists(self, title, exclude_index=None):
        """Return True if a task with the same title (case-insensitive) already exists.
        exclude_index lets update() ignore the task being edited."""
        title_norm = title.strip().lower()
        for i, t in enumerate(self.tasks):
            if i == exclude_index:
                continue
            if t.get("title", "").strip().lower() == title_norm:
                return True
        return False

    def is_duplicate(self, title, exclude_index=None):
        """Public check: True if a task with the same title already exists (case-insensitive)."""
        return self._title_exists(title, exclude_index=exclude_index)

    def add(self, title, category):
        title = title.strip()
        if not title:
            return None
        if category not in CATEGORIES:
            return None

        if self._title_exists(title):
            return None  # duplicate

        task = {"title": title, "category": category, "status": DEFAULT_STATUS}
        self.tasks.append(task)
        self._save()
        return task

    def update(self, index, title=None, category=None, status=None):
        task = self._task_at(index)
        if task is None:
            return None

        if title is not None:
            title = title.strip()
            if not title:
                return None
            if self._title_exists(title, exclude_index=index):
                return None  # duplicate
        if category is not None and category not in CATEGORIES:
            return None
        if status is not None and status not in STATUSES:
            return None

        has_changes = False
        if title is not None and title != task.get("title"):
            task["title"] = title
            has_changes = True
        if category is not None and category != task.get("category"):
            task["category"] = category
            has_changes = True
        if status is not None and status != task.get("status"):
            task["status"] = status
            has_changes = True

        if has_changes:
            self._save()
        return task

    def delete(self, index):
        task = self._task_at(index)
        if task is None:
            return None

        self.tasks.remove(task)
        self._save()
        return task

    def rows(self):
        return list(self.tasks)

    def progress(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.get("status") == "Completed")
        percent = int(round(done / total * 100)) if total else 0
        return done, total, percent

    def progress_text(self):
        done, total, percent = self.progress()
        return f"{done}/{total} completed ({percent}%)"

    def _task_at(self, index):
        if not isinstance(index, int):
            return None
        if index < 0 or index >= len(self.tasks):
            return None
        return self.tasks[index]

    def _load(self):
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return []
        except OSError as err:
            print(f"[ERROR] Could not read {self.path}: {err}")
            return []

        if not text.strip():
            return []

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            print(f"[ERROR] {self.path} is not valid JSON, starting empty")
            self._quarantine()
            return []

        if not isinstance(parsed, list):
            print(f"[ERROR] {self.path} does not hold a task list, starting empty")
            self._quarantine()
            return []

        return [t for t in parsed if isinstance(t, dict)]

    def _quarantine(self):
        backup = self.path.with_name(self.path.name + ".corrupt")
        try:
            self.path.replace(backup)
            print(f"[WARN] Unreadable data moved aside to {backup}")
        except OSError as err:
            print(f"[ERROR] Could not set aside {self.path}: {err}")

    def _save(self):
        tmp = self.path.with_name(self.path.name + ".tmp")
        try:
            tmp.write_text(json.dumps(self.tasks, indent=2), encoding="utf-8")
            tmp.replace(self.path)
        except OSError as err:
            print(f"[ERROR] Could not write {self.path}: {err}")


class TaskManagerApp:
    def __init__(self, root, store=None):
        self.root = root
        self.store = store if store is not None else TaskStore()

        self.root.title("Task Manager")
        self.root.geometry("700x460")

        self.create_input_frame()
        self.create_button_frame()
        self.create_table_frame()
        self.create_status_frame()

        self.refresh_table()

    def create_input_frame(self):
        pambasa = tk.Frame(self.root, pady=10)
        pambasa.pack(fill=tk.X, padx=20)

        tk.Label(pambasa, text="Task:").grid(row=0, column=0, padx=5, sticky="e")
        self.title_entry = tk.Entry(pambasa, width=52)
        self.title_entry.grid(row=0, column=1, columnspan=3, padx=5, sticky="we")
        self.title_entry.bind("<Return>", lambda event: self.add_task())
        self.title_entry.bind("<KeyRelease>", self.on_title_typed)
        tk.Label(pambasa, text="Category:").grid(row=1, column=0, padx=5, pady=6, sticky="e")
        self.combo_category = ttk.Combobox(
            pambasa, values=list(CATEGORIES), state="readonly", width=18
        )
        self.combo_category.current(0)
        self.combo_category.grid(row=1, column=1, padx=5, pady=6, sticky="w")

        tk.Label(pambasa, text="Status:").grid(row=1, column=2, padx=5, pady=6, sticky="e")
        self.combo_status = ttk.Combobox(
            pambasa, values=list(STATUSES), state="readonly", width=15
        )
        self.combo_status.current(0)
        self.combo_status.grid(row=1, column=3, padx=5, pady=6, sticky="w")

        pambasa.columnconfigure(1, weight=1)

    def create_button_frame(self):
        pindutan = tk.Frame(self.root)
        pindutan.pack(fill=tk.X, padx=25, pady=(0, 10))

        for hanay, (sulat, kilos) in enumerate(
            [
                ("Add Task", self.add_task),
                ("Update Task", self.update_task),
                ("Delete Task", self.delete_task),
                ("Show Progress", self.show_progress),
            ]
        ):
            tk.Button(pindutan, text=sulat, command=kilos, width=14).grid(
                row=0, column=hanay, padx=3
            )

    def create_table_frame(self):
        lamesa = tk.Frame(self.root)
        lamesa.pack(fill=tk.BOTH, expand=True, padx=20)

        garotos = ttk.Scrollbar(lamesa, orient="vertical")

        self.tree = ttk.Treeview(
            lamesa,
            columns=("#", "Task", "Category", "Status"),
            show="headings",
            selectmode="browse",
            yscrollcommand=garotos.set,
        )
        garotos.config(command=self.tree.yview)

        self.tree.heading("#", text="Uncle Dags")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")

        self.tree.column("#", width=45, anchor="center", stretch=False)
        self.tree.column("Task", width=280)
        self.tree.column("Category", width=140, anchor="center")
        self.tree.column("Status", width=130, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        garotos.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=garotos.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_status_frame(self):
        self.status_label = tk.Label(self.root, text="", pady=6)
        self.status_label.pack(fill=tk.X)

    def show_status(self, mensahe):
        self.status_label.config(text=mensahe)

    def clear_status(self):
        self.status_label.config(text="")

    def selected_index(self, tahimik=False):
        napili = self.tree.selection()
        if not napili:
            if not tahimik:
                messagebox.showerror(
                    "Selection Error", "Please select a task from the list first."
                )
            return None
        return int(napili[0])

    def on_select(self, evento):
        index = self.selected_index(tahimik=True)
        if index is None:
            return

        mga_gawain = self.store.rows()
        if index < 0 or index >= len(mga_gawain):
            return
        gawain = mga_gawain[index]

        self.clear_status()
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, gawain["title"])
        self.combo_category.set(gawain["category"])
        self.combo_status.set(gawain["status"])

    def on_title_typed(self, evento):
        if self.title_entry.get().strip():
            self.clear_status()

    def add_task(self):
        title = self.title_entry.get().strip()
        category = self.combo_category.get()

        if not title:
            messagebox.showerror("Input Error", "Please enter a task title.")
            return
        if category not in CATEGORIES:
            messagebox.showerror(
                "Input Error", f"Please choose a category: {', '.join(CATEGORIES)}."
            )
            return

        if self.store.is_duplicate(title):
            messagebox.showerror(
                "Duplicate Task",
                f"'{title}' already exists in your tasks. Please use a different title.",
            )
            return

        saved_task = self.store.add(title, category)
        if saved_task is None:
            messagebox.showerror("Input Error", "Could not add this task.")
            return

        self.refresh_table()
        self.clear_entries()
        messagebox.showinfo("Success", f"Added '{title}' to your tasks.")

    def update_task(self):
        index = self.selected_index()
        if index is None:
            return

        title = self.title_entry.get().strip()
        if not title:
            self.show_status("Title cannot be empty. Nothing was changed.")
            return

        tasks = self.store.rows()
        if index < 0 or index >= len(tasks):
            return
        task = tasks[index]

        category = self.combo_category.get()
        status = self.combo_status.get()

        if (title, category, status) == (task["title"], task["category"], task["status"]):
            self.show_status("No changes to save.")
            return

        if self.store.is_duplicate(title, exclude_index=index):
            messagebox.showerror(
                "Duplicate Task",
                f"'{title}' already exists in your tasks. Please use a different title.",
            )
            return

        saved_task = self.store.update(
            index, title=title, category=category, status=status
        )
        if saved_task is None:
            self.show_status("Could not update this task. Nothing was changed.")
            return

        self.clear_status()
        self.refresh_table()
        self.tree.selection_set(str(index))
        messagebox.showinfo("Success", f"Updated '{saved_task['title']}'.")

    def delete_task(self):
        index = self.selected_index()
        if index is None:
            return

        tasks = self.store.rows()
        if index < 0 or index >= len(tasks):
            return
        task_title = tasks[index]["title"]

        if not messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete '{task_title}'?"
        ):
            return

        self.store.delete(index)
        self.clear_status()
        self.refresh_table()
        self.clear_entries()
        messagebox.showinfo("Success", f"Deleted '{task_title}'.")

    def show_progress(self):
        messagebox.showinfo("Progress", self.store.progress_text())

    def refresh_table(self):
        for kalat in self.tree.get_children():
            self.tree.delete(kalat)

        for hanay, gawain in enumerate(self.store.rows()):
            self.tree.insert(
                "",
                tk.END,
                iid=str(hanay),
                values=(
                    hanay + 1,
                    gawain["title"],
                    gawain["category"],
                    gawain["status"],
                ),
            )

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.combo_category.current(0)
        self.combo_status.current(0)
        self.clear_status()


if __name__ == "__main__":
    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()