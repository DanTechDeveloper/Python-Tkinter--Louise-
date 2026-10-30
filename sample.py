from pathlib import Path
import json
import os

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Keep the JSON file beside this script, no matter where you run it from.
DATA_FILE = Path(__file__).with_name("sample.json")


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Sample")

        # --- computed values (state) ---
        self.yearPriceHolder = 0
        self.unitCostHolder = 0
        self.unitCostArray = []
        self.labHolder = 0
        self.cashHolder = 0
        self.gettingDiscount = 0
        self.totalOverall = 0

        # --- "database": read the JSON ONCE on startup ---
        self.records = self.load_records()

        # --- form ---
        self.yearLevelLabel = self.create_label("Year Level")
        self.yearLevel = self.create_combobox(['1st Year - 1,500 php', '2nd Year - 2,000 php', '3rd Year - 3,000 php', '4th Year - 4,000 php'])
        self.yearLevel.current(0)
        self.subject = self.create_label("How many subjects do you have")
        self.subjectCount = self.create_textbox()
        self.subjectCountButton = self.create_button("CONFIRM", self.setSubjectCount)

        # Dynamic inputs (unit costs, lab, cash, SUBMIT) are rebuilt inside this frame.
        self.detailsFrame = ttk.Frame(self.root)
        self.detailsFrame.pack(fill="x")
        self.popupButton = self.create_button("CLICK ME", self.clickMe)
        # Table is created ONCE, then filled from the records loaded at startup.
        self.table = self.create_table(("Year Level", "Unit Cost", "Laboratory", "Cash Discount", "Total"))
        self.refresh_table()

    # ------------------------------------------------------------------
    # JSON "database" helpers
    # ------------------------------------------------------------------
    
    def clickMe(self):
        root = Tk()
        root.title("Hello World")
        self.create_label("Tangina Mo Jepoy Dizon", root)
        root.mainloop();
    def load_records(self):
        """Read sample.json once. Returns a list of records."""
        if not DATA_FILE.exists():
            return []

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            messagebox.showerror("Load error", f"Could not read {DATA_FILE.name}:\n{error}")
            return []

        if not isinstance(data, list):
            messagebox.showerror("Load error", f"{DATA_FILE.name} must contain a list of records.")
            return []

        return data

    def save_records(self):
        """Write the whole in-memory list back to sample.json (atomically)."""
        temp_file = DATA_FILE.with_suffix(DATA_FILE.suffix + ".tmp")
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(self.records, file, indent=2)
        os.replace(temp_file, DATA_FILE)  # avoids a half-written JSON file

    @staticmethod
    def row_values(record):
        return (
            record.get("yearPriceHolder", 0),
            record.get("unitCostHolder", 0),
            record.get("labHolder", 0),
            record.get("gettingDiscount", 0),
            record.get("totalOverall", 0),
        )

    def refresh_table(self):
        """Clear the table and draw every record currently in memory."""
        for item in self.table.get_children():
            self.table.delete(item)
        for record in self.records:
            self.table.insert("", "end", values=self.row_values(record))

    # ------------------------------------------------------------------
    # Form logic
    # ------------------------------------------------------------------
    def setSubjectCount(self):
        try:
            subjectCount = int(self.subjectCount.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid whole number of subjects.")
            return

        if subjectCount <= 0:
            messagebox.showerror("Invalid input", "Number of subjects must be at least 1.")
            return

        yearPrices = {
            "1st Year - 1,500 php": 1500,
            "2nd Year - 2,000 php": 2000,
            "3rd Year - 3,000 php": 3000,
            "4th Year - 4,000 php": 4000,
        }
        self.yearPriceHolder = yearPrices.get(self.yearLevel.get(), 0)

        # Rebuild the dynamic part so pressing CONFIRM again does not duplicate widgets.
        for widget in self.detailsFrame.winfo_children():
            widget.destroy()
        self.unitCostArray = []

        for i in range(subjectCount):
            self.create_label(f"Unit Cost subject {i + 1}: ", self.detailsFrame)
            unitCost = self.create_textbox(self.detailsFrame)
            self.unitCostArray.append(unitCost)

        self.create_label("With laboratory?", self.detailsFrame)
        self.lab = self.create_combobox(['Yes (+ 500php)', 'No (0 php)'], self.detailsFrame)
        self.lab.current(1)

        self.create_label("Cash?", self.detailsFrame)
        self.cash = self.create_combobox(["Yes (10% Discount)", "No (0% Discount)"], self.detailsFrame)
        self.cash.current(0)

        self.create_button("SUBMIT", self.total, self.detailsFrame)

    def total(self):
        try:
            unitCosts = [int(entry.get()) for entry in self.unitCostArray]
        except ValueError:
            messagebox.showerror("Invalid input", "Every unit cost must be a whole number.")
            return

        self.unitCostHolder = sum(unitCosts)

        if self.lab.get() == "Yes (+ 500php)":
            self.labHolder = 500
        elif self.lab.get() == "No (0 php)":
            self.labHolder = 0

        if self.cash.get() == "Yes (10% Discount)":
            self.cashHolder = 0.10
        elif self.cash.get() == "No (0% Discount)":
            self.cashHolder = 0

        self.totalOverall = self.yearPriceHolder + self.unitCostHolder + self.labHolder
        self.gettingDiscount = round(self.totalOverall * self.cashHolder, 2)
        self.totalOverall = round(self.totalOverall - self.gettingDiscount, 2)

        record = {
            "yearPriceHolder": self.yearPriceHolder,
            "unitCostHolder": self.unitCostHolder,
            "labHolder": self.labHolder,
            "gettingDiscount": self.gettingDiscount,
            "totalOverall": self.totalOverall,
        }

        # Append to memory, then persist the whole list once.
        self.records.append(record)
        try:
            self.save_records()
        except OSError as error:
            self.records.pop()
            messagebox.showerror("Save error", f"Could not write {DATA_FILE.name}:\n{error}")
            return

        # Add only the new row; do NOT re-read the file.
        self.table.insert("", "end", values=self.row_values(record))

    # ------------------------------------------------------------------
    # Widget factories
    # ------------------------------------------------------------------
    def create_label(self, text, parent=None):
        label = ttk.Label(parent or self.root, text=text)
        label.pack()
        return label

    def create_button(self, text, command, parent=None):
        button = ttk.Button(parent or self.root, text=text, command=command)
        button.pack()
        return button

    def create_textbox(self, parent=None):
        textbox = ttk.Entry(parent or self.root)
        textbox.pack()
        return textbox

    def create_combobox(self, values, parent=None):
        combobox = ttk.Combobox(parent or self.root, values=values)
        combobox.pack()
        return combobox

    def create_table(self, columns):
        table = ttk.Treeview(self.root, columns=columns, show="headings")
        for column in columns:
            table.heading(column, text=column)
            table.column(column, width=120, anchor="center")
        table.pack()
        return table

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GUI()
    app.run()
