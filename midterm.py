import sqlite3
import random
import tkinter as tk
from tkinter import messagebox, ttk
import datetime


class LibraryDatabase:


    def __init__(self, db_name="theHellsssss.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
      
    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS table_one (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                author TEXT NOT NULL,
                status TEXT NOT NULL,
                borrowed_by TEXT
            )
        """
        )
        self.conn.commit()


        self.cursor.execute("SELECT COUNT(*) FROM table_one")
        if self.cursor.fetchone()[0] == 0:
            initial_books = [
                ("Java Programming", "James Gosling", "Available", None),
                ("AI Architecture", "Harper Lee", "Available", None),
                ("Data Science Basics", "George Orwell", "Available", None),
                ("To Kill a Mockingbird", "Harper Lee", "Available", None),
                ("1984", "George Orwell", "Available", None),
                ("The Lord of the Rings", "J.R.R. Tolkien", "Available", None),
                ("The Catcher in the Rye", "J.D. Salinger", "Available", None),
                ("The Great Gatsby", "F. Scott Fitzgerald", "Available", None),
                ("The Lion, the Witch and the Wardrobe", "C.S. Lewis", "Available", None),
                ("Lord of the Flies", "William Golding", "Available", None),
                ("Animal Farm", "George Orwell", "Available", None),
                ("Catch-22", "Joseph Heller", "Available", None),
                ("The Grapes of Wrath", "John Steinbeck", "Available", None),
                ("Gone with the Wind", "Margaret Mitchell", "Available", None),
                ("Slaughterhouse-Five", "Kurt Vonnegut Jr.", "Available", None),
                ("One Flew Over the Cuckoo's Nest", "Ken Kesey", "Available", None),
                ("A Clockwork Orange", "Anthony Burgess", "Available", None),
                ("Lolita", "Vladimir Nabokov", "Available", None),
                ("Are You There God? It's Me, Margaret", "Judy Blume", "Available", None),
                ("Atonement", "Ian McEwan", "Available", None),
                ("Watchmen", "Alan Moore", "Available", None),
                ("Never Let Me Go", "Kazuo Ishiguro", "Available", None),
                ("Charlotte's Web", "E.B. White", "Available", None),
                ("The True Story of the 3 Little Pigs", "Jon Scieszka", "Available", None),
                ("Beloved", "Toni Morrison", "Available", None),
                ("Misery", "Stephen King", "Available", None),
                ("Mort", "Terry Pratchett", "Available", None),
                ("The Drawing of the Three", "Stephen King", "Available", None),
                ("Equal Rites", "Terry Pratchett", "Available", None),
                ("Calvin and Hobbes", "Bill Watterson", "Available", None),
                ("Fried Green Tomatoes at the Whistle Stop Cafe", "Fannie Flagg", "Available", None),
                ("The Bonfire of the Vanities", "Tom Wolfe", "Available", None),
                ("The Complete Maus", "Art Spiegelman", "Available", None),
                ("Patriot Games", "Tom Clancy", "Available", None),
                ("The Long Walk", "Richard Bachman", "Available", None),
                ("Norwegian Wood", "Haruki Murakami", "Available", None),
                ("Hatchet", "Gary Paulsen", "Available", None),
                ("Consider Phlebas", "Iain M. Banks", "Available", None),
                ("Dirk Gently's Holistic Detective Agency", "Douglas Adams", "Available", None),
                ("Moon Tiger", "Penelope Lively", "Available", None),
                ("The New York Trilogy", "Paul Auster", "Available", None),
                ("The 7 Habits of Highly Effective People", "Stephen R. Covey", "Available", None),
                ("How to Win Friends & Influence People", "Dale Carnegie", "Available", None),
                ("The Alchemist", "Paulo Coelho", "Available", None),
                ("Think and Grow Rich", "Napoleon Hill", "Available", None),
                ("The Power of Now", "Eckhart Tolle", "Available", None),
                ("Oh, the Places You'll Go!", "Dr. Seuss", "Available", None),
                ("Getting Things Done", "David Allen", "Available", None),
                ("The Purpose Driven Life", "Rick Warren", "Available", None),
                ("The Four Agreements", "Miguel Ruiz", "Available", None),
                ("As a Man Thinketh", "James Allen", "Available", None),
                ("Man's Search for Meaning", "Viktor E. Frankl", "Available", None),
                ("The Secret", "Rhonda Byrne", "Available", None),
                ("Tuesdays with Morrie", "Mitch Albom", "Available", None),
                ("The Art of Happiness", "Dalai Lama XIV", "Available", None),
                ("Lean In", "Sheryl Sandberg", "Available", None),
                ("The Shining", "Stephen King", "Available", None),
                ("It", "Stephen King", "Available", None),
                ("The Stand", "Stephen King", "Available", None),
                ("Dune", "Frank Herbert", "Available", None),
                ("Neuromancer", "William Gibson", "Available", None),
                ("Snow Crash", "Neal Stephenson", "Available", None),
            ]
            self.cursor.executemany(
                "INSERT INTO table_one (title, author, status, borrowed_by) VALUES (?, ?, ?, ?)",
                initial_books
            )
            self.conn.commit()

            students = [
                "Dan", "Mark", "John", "Doe", "Solis", "Cruz", "Reyes", "Garcia",
                "Lopez", "Perez", "Hernandez", "Gonzalez", "Sanchez", "Ramirez",
                "Torres", "Flores", "Rivera", "Gomez", "Morales", "Ortiz", "Ruiz",
                "Vasquez", "Brown", "Davis", "Keybert", "Vincent", "Raffy", "Gelo",
                "Yuri",
            ]
            self.cursor.execute("SELECT rowid, title FROM table_one WHERE status='Available'")
            available_books = self.cursor.fetchall()
            selected = random.sample(available_books, min(30, len(available_books)))
            for rowid, title in selected:
                student = random.choice(students)
                self.cursor.execute(
                    "UPDATE table_one SET status='Borrowed', borrowed_by=? WHERE rowid=?",
                    (student, rowid),
                )
            self.conn.commit()

    def fetch_all(self, query_str=""):
        if query_str:
            term = f"%{query_str}%"
            self.cursor.execute(
                "SELECT title, author, status, borrowed_by FROM table_one WHERE title LIKE ? OR author LIKE ? OR borrowed_by LIKE ?",
                (term, term, term),
            )
        else:
            self.cursor.execute("SELECT title, author, status, borrowed_by FROM table_one")
        return self.cursor.fetchall()

    def add_book(self, title, author):
        try:
            self.cursor.execute(
                "INSERT INTO table_one (title, author, status, borrowed_by) VALUES (?, ?, ?, ?)",
                (title, author, "Available", None),
            )
            self.conn.commit()
            return True, "Book added successfully."
        except sqlite3.IntegrityError:
            return False, f"'{title}' already exists in the library."

    def update_status(self, title, new_status, borrowed_by=None):
        if new_status == "Available":
            borrowed_by = "N/A"
        self.cursor.execute(
            "UPDATE table_one SET status = ?, borrowed_by = ? WHERE title = ?",
            (new_status, borrowed_by, title),
        )
        self.conn.commit()

    def delete_book(self, title):
        self.cursor.execute("DELETE FROM table_one WHERE title = ?", (title,))
        self.conn.commit()

    def get_book_status(self, title):
        self.cursor.execute(
            "SELECT status FROM table_one WHERE title = ?", (title,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()


class LibrarySystem:

    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library Management System")
        self.root.geometry("680x520")
        self.root.config(bg="#F4F6F9")


        self.db = LibraryDatabase()


        self.setup_styles()


        self.create_header()
        self.create_search_frame()
        self.create_input_frame()
        self.create_button_frame()
        self.create_table_frame()


        self.refresh_table()
        self.update_borrow_button_state()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")


        style.configure(
            "Treeview.Heading",
            font=("Helvetica", 10, "bold"),
            background="#2C3E50",
            foreground="white",
        )
        style.configure(
            "Treeview", font=("Helvetica", 10), rowheight=25, fieldbackground="white"
        )
        style.map("Treeview", background=[("selected", "#3498DB")])

    def create_header(self):
        header = tk.Label(
            self.root,
            text="📚 Library Management System",
            font=("Helvetica", 16, "bold"),
            bg="#2C3E50",
            fg="white",
            pady=12,
        )
        header.pack(fill=tk.X)

    def create_search_frame(self):
        search_frame = tk.Frame(self.root, bg="#F4F6F9", pady=5)
        search_frame.pack(fill=tk.X, padx=20)

        tk.Label(
            search_frame,
            text="Search:",
            bg="#F4F6F9",
            font=("Helvetica", 10, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_table())

        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, width=30
        )
        search_entry.pack(side=tk.LEFT, padx=5)

    def create_input_frame(self):
        input_frame = tk.Frame(self.root, bg="#F4F6F9", pady=5)
        input_frame.pack()

        tk.Label(
            input_frame,
            text="Book Title:",
            bg="#F4F6F9",
            font=("Helvetica", 10, "bold"),
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            input_frame,
            text="Author:",
            bg="#F4F6F9",
            font=("Helvetica", 10, "bold"),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

    def create_button_frame(self):
        btn_frame = tk.Frame(self.root, bg="#F4F6F9", pady=10)
        btn_frame.pack()

        btn_specs = [
            ("Add Book", self.add_book, "#2ECC71"),
            ("Borrow Book", self.borrow_book, "#E67E22"),
            ("Return Book", self.return_book, "#3498DB"),
            ("Delete Book", self.delete_book, "#E74C3C"),
            ("Clear Form", self.clear_entries, "#95A5A6"),
            ("Reports", self.reports, "#1B4F72"),
        ]

        for idx, (text, command, color) in enumerate(btn_specs):
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Helvetica", 9, "bold"),
                width=11,
                relief="flat",
                cursor="hand2",
            )
            btn.grid(row=0, column=idx, padx=4)
            if text == "Borrow Book":
                self.borrow_btn = btn

    def create_table_frame(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 15))


        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Title", "Author", "Status", "Borrowed By"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("Title", text="Book Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Borrowed By", text="Borrowed By")

        self.tree.column("Title", width=250)
        self.tree.column("Author", width=200)
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Borrowed By", width=150, anchor="w")

        self.tree.tag_configure(
            "Available", background="#E8F8F5", foreground="#117A65"
        )
        self.tree.tag_configure(
            "Borrowed", background="#FDEDEC", foreground="#C0392B"
        )

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_query = self.search_var.get().strip()
        books = self.db.fetch_all(search_query)

        for title, author, status, borrowed_by in books:
            stats = "N/A" if borrowed_by == None else borrowed_by
            self.tree.insert(
                "",
                tk.END,
                values=(title, author, status, stats),
                tags=(status,),
            )

        self.update_borrow_button_state()

    def update_borrow_button_state(self):
        if not hasattr(self, 'borrow_btn'):
            return
        selected_item = self.tree.selection()
        if selected_item:
            selected = self.tree.item(selected_item[0])["values"][0]
            status = self.db.get_book_status(selected)
        else:
            status = None
        if status == "Available":
            self.borrow_btn.config(state=tk.NORMAL)
        else:
            self.borrow_btn.config(state=tk.DISABLED)

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])["values"]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[0])

            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, values[1])

            self.update_borrow_button_state()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()

        if not title or not author:
            messagebox.showwarning(
                "Input Error", "Please enter both Title and Author."
            )
            return
        success, msg = self.db.add_book(title, author)
        if success:
            self.refresh_table()
            self.clear_entries()
            messagebox.showinfo("Success", f"Added '{title}' to the library.")
        else:
            messagebox.showerror("Error", msg)

    def borrow_book(self):
        selected = self.get_selected_title()
        if selected:
            status = self.db.get_book_status(selected)
            if status == "Borrowed":
                messagebox.showwarning(
                    "Warning", f"'{selected}' is already borrowed."
                )
            elif status == "Available":
                self.db.update_status(selected, "Borrowed", "N/A")
                self.refresh_table()
                self.clear_entries()
                messagebox.showinfo("Success", f"You borrowed '{selected}'.")

    def return_book(self):
        selected = self.get_selected_title()
        if selected:
            status = self.db.get_book_status(selected)
            if status == "Available":
                messagebox.showwarning("Warning", f"'{selected}' was not borrowed.")
            elif status == "Borrowed":
                self.db.update_status(selected, "Available")
                self.refresh_table()
                self.clear_entries()
                messagebox.showinfo("Success", f"You returned '{selected}'.")

    def delete_book(self):
        selected = self.get_selected_title()
        if selected:
            if messagebox.askyesno(
                    "Confirm Delete", f"Are you sure you want to delete '{selected}'?"
            ):
                self.db.delete_book(selected)
                self.refresh_table()
                self.clear_entries()
                messagebox.showinfo("Success", f"Deleted '{selected}'.")

    def get_selected_title(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])["values"][0]

        entry_title = self.title_entry.get().strip()
        if self.db.get_book_status(entry_title):
            return entry_title

        messagebox.showwarning(
            "Selection Error",
            "Please select a book from the list or enter a valid title.",
        )
        return None

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())
        self.update_borrow_button_state()
        
    def reports(self):
        # Connect to database
        conn = sqlite3.connect("theHellsssss.db")
        cursor = conn.cursor()

        # Get today's date
        today = datetime.date.today()

        # 1. Total Books
        cursor.execute("SELECT COUNT(*) FROM table_one")
        total_books = cursor.fetchone()[0]

        # 2. Available Books
        cursor.execute("SELECT COUNT(*) FROM table_one WHERE status='Available'")
        available_books = cursor.fetchone()[0]

        # 3. Borrowed Books
        cursor.execute("SELECT COUNT(*) FROM table_one WHERE status='Borrowed'")
        borrowed_books = cursor.fetchone()[0]

        # 4. List of Borrowers
        cursor.execute(
        "SELECT DISTINCT borrowed_by "
        "FROM table_one "
        "WHERE borrowed_by IS NOT NULL "
        "ORDER BY borrowed_by"
        )
        borrowers = [row[0] for row in cursor.fetchall()]

        # 6. List of Currently Borrowed Books
        cursor.execute(
            "SELECT title, borrowed_by "
            "FROM table_one "
            "WHERE status='Borrowed' "
            "ORDER BY title"
        )
        borrowed_list = cursor.fetchall()

        conn.close()

        # Create new window for reports
        reports_window = tk.Toplevel(self.root)
        reports_window.title("Library Reports")
        reports_window.geometry("900x650")
        reports_window.config(bg="#F4F6F9")

        # Header
        header = tk.Frame(reports_window, bg="#2C3E50", pady=15)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="📊 Library System Reports",
            font=("Helvetica", 20, "bold"),
            bg="#2C3E50",
            fg="white",
        ).pack()
        tk.Label(
            header,
            text=f"As of {today.strftime('%B %d, %Y')}",
            font=("Helvetica", 10),
            bg="#2C3E50",
            fg="#BDC3C7",
        ).pack()

        # Main Frame
        main_frame = tk.Frame(reports_window, bg="#F4F6F9")
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Left Frame (Statistics + Borrowers)
        left_frame = tk.Frame(main_frame, bg="#F4F6F9")
        left_frame.pack(side=tk.LEFT, padx=(0, 10), fill=tk.BOTH, expand=True)

        # Statistics Frame
        stats_frame = tk.LabelFrame(
            left_frame, text="  📈 Statistics  ", font=("Helvetica", 11, "bold"),
            bg="#F4F6F9", fg="#2C3E50", padx=15, pady=15
        )
        stats_frame.pack(pady=(0, 15), fill=tk.X)

        stat_cards = [
            ("📚 Total Books", total_books, "#3498DB", "white"),
            ("✅ Available", available_books, "#2ECC71", "white"),
            ("📖 Borrowed", borrowed_books, "#E74C3C", "white"),
        ]

        for idx, (label, value, bg_color, fg_color) in enumerate(stat_cards):
            card = tk.Frame(stats_frame, bg=bg_color, padx=15, pady=10)
            card.pack(fill=tk.X, pady=5)
            tk.Label(
                card, text=label, font=("Helvetica", 10, "bold"),
                bg=bg_color, fg=fg_color
            ).pack(side=tk.LEFT)
            tk.Label(
                card, text=str(value), font=("Helvetica", 14, "bold"),
                bg=bg_color, fg=fg_color
            ).pack(side=tk.RIGHT)

        # Borrowers List Frame
        borrowers_frame = tk.LabelFrame(
            left_frame, text=f"  👥 Borrowers List ({len(borrowers)})  ",
            font=("Helvetica", 11, "bold"), bg="#F4F6F9", fg="#2C3E50",
            padx=10, pady=10
        )
        borrowers_frame.pack(fill=tk.BOTH, expand=True)

        borrowers_listbox = tk.Listbox(
            borrowers_frame, width=35, height=12,
            font=("Helvetica", 10), bg="white", fg="#2C3E50",
            selectbackground="#3498DB", selectforeground="white",
            relief="flat", borderwidth=5
        )
        borrowers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        borrowers_scrollbar = ttk.Scrollbar(borrowers_frame, orient=tk.VERTICAL, command=borrowers_listbox.yview)
        borrowers_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        borrowers_listbox.config(yscrollcommand=borrowers_scrollbar.set)

        for student in borrowers:
            borrowers_listbox.insert(tk.END, f"  {student}")

        # Right Frame (Borrowed Books)
        borrowed_frame = tk.LabelFrame(
            main_frame, text="  📋 Currently Borrowed Books  ",
            font=("Helvetica", 11, "bold"), bg="#F4F6F9", fg="#2C3E50",
            padx=10, pady=10
        )
        borrowed_frame.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.BOTH, expand=True)

        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Report.Treeview",
            font=("Helvetica", 10),
            rowheight=25,
            background="white",
            foreground="#2C3E50",
            fieldbackground="white"
        )
        style.configure(
            "Report.Treeview.Heading",
            font=("Helvetica", 10, "bold"),
            background="#2C3E50",
            foreground="white"
        )
        style.map("Report.Treeview", background=[("selected", "#3498DB")])

        borrowed_tree = ttk.Treeview(
            borrowed_frame, columns=("Title", "Borrowed By"),
            show="headings", style="Report.Treeview"
        )
        borrowed_tree.heading("Title", text="Book Title")
        borrowed_tree.heading("Borrowed By", text="Borrowed By")
        borrowed_tree.column("Title", width=280, anchor="w")
        borrowed_tree.column("Borrowed By", width=120, anchor="w")
        borrowed_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        borrowed_scrollbar = ttk.Scrollbar(borrowed_frame, orient=tk.VERTICAL, command=borrowed_tree.yview)
        borrowed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        borrowed_tree.config(yscrollcommand=borrowed_scrollbar.set)

        for title, borrower in borrowed_list:
            borrowed_tree.insert("", tk.END, values=(title, borrower))


if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)


    
    def on_closing():
        app.db.close()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    