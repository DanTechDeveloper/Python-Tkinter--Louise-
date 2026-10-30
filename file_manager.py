import pathlib


class ManagedFile:
    """Guard that guarantees the file is closed on scope exit."""

    def __init__(self, filepath: str | pathlib.Path, mode: str = "r", encoding: str = "utf-8"):
        self.filepath = pathlib.Path(filepath)
        self.mode = mode
        self.encoding = encoding
        self.file = None

    def __enter__(self):
        print(f"[OPENING] file in {self.mode} mode {self.filepath}\n")
        self.file = open(self.filepath, self.mode, encoding=self.encoding)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Guard-close: always attempt close, no matter how we exited
        if self.file is None:
            return False
        try:
            print("\n[CLOSING] file")
            if not self.file.closed:
                self.file.close()
        except Exception as e:
            print(f"Error closing file: {e}")
        return False  # never suppress original exception

    def close(self):
        """Manual guard-close for non-with usage."""
        if self.file and not self.file.closed:
            self.file.close()


def _write(path: pathlib.Path):
    content = input("Enter content to overwrite the file: ")
    try:
        with ManagedFile(path, "w") as f:
            f.write(content)
            f.write("\n")
    except OSError as e:
        print(f"[ERROR] Could not write to {path}: {e}")


def _append(path: pathlib.Path):
    content = input("Enter content to append: ")
    try:
        with ManagedFile(path, "a") as f:
            f.write(content)
            f.write("\n")
    except OSError as e:
        print(f"[ERROR] Could not append to {path}: {e}")


def _read(path: pathlib.Path):
    try:
        with ManagedFile(path, "r") as f:
            print(f.read())
            print()
    except FileNotFoundError:
        print(f"File {path} not found")
    except IsADirectoryError:
        print(f"[ERROR] {path} is a directory")
    except OSError as e:
        print(f"[ERROR] Could not read {path}: {e}")


def _delete(path: pathlib.Path):
    # Guard clauses — fail fast, flat control flow
    if not path.exists():
        print(f"File {path} does not exist")
        return
    if path.is_dir():
        print(f"[ERROR] {path} is a directory, not deleting")
        return
    confirm = input(f"Are you sure you want to delete this file {path}? (y/n): ").strip().lower()
    if confirm != "y":
        print("File not deleted")
        return
    try:
        path.unlink()
        print("file deleted successfully")
    except OSError as e:
        print(f"[ERROR] Could not delete {path}: {e}")


if __name__ == "__main__":
    raw = input("Enter the filename:  (eg. my_notes.txt): ").strip()
    if not raw:
        print("Filename cannot be empty")
        raise SystemExit(1)

    filepath = pathlib.Path(raw)

    while True:
        choice = input(
            "1. Write text (overwrite)\n2.Append text\n3. Read from file\n4. Delete file\n5. Exit\n Enter your choice: "
        ).strip()

        # Guard clauses for menu — no deep elif ladder
        if choice not in {"1", "2", "3", "4", "5"}:
            print("Invalid choice")
            continue
        if choice == "5":
            print("Exiting...")
            break
        if choice == "1":
            _write(filepath)
            continue
        if choice == "2":
            _append(filepath)
            continue
        if choice == "3":
            _read(filepath)
            continue
        if choice == "4":
            _delete(filepath)
            continue
