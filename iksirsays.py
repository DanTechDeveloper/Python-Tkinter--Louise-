from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class Iksirsays:
    def __init__(self):
        self.root = Tk()
        self.root.title("Iksirsays Program")
        self.title = ttk.Label(self.root, text = "Simple Counter")
        self.title.pack()
        self.counter = 0
        self.number = ttk.Label(self.root, text = self.counter)
        self.number.pack()
        self.increment = ttk.Button(self.root, text = "Increment", command=self.increment)
        self.increment.pack()
        self.decrement = ttk.Button(self.root, text="Decrement", command=self.decrement)
        self.decrement.pack()
        self.reset = ttk.Button(self.root, text="Reset", command=self.reset)
        self.reset.pack()
        self.username = ttk.Label(self.root, text="Enter A Username")
        self.username.pack()
        self.textbox_userName = ttk.Entry(self.root)
        self.textbox_userName.pack()
        self.password = ttk.Label(self.root, text="Enter A Password")
        self.password.pack()
        self.textbox_password = ttk.Entry(self.root)
        self.textbox_password.pack()
        self.submit = ttk.Button(self.root, text="Submit", command=self.submit)
        self.submit.pack()
        self.ArrayGrade = []
        for i in range(3):
            self.gradeLabel = ttk.Label(self.root, text=f"Enter Grade {i + 1}")
            self.gradeLabel.pack()
            self.grades = ttk.Entry(self.root)
            self.grades.pack()
            self.ArrayGrade.append(self.grades)
            
        self.gradesButton = ttk.Button(self.root, text="SUBMIT GRADE", command=self.calculateGrade)
        self.gradesButton.pack()
        
        
        self.labelTaskManager = ttk.Label(self.root, text="Task Manager")
        self.labelTaskManager.pack()
        self.taskManagerCounter = 0
        self.labelTask = ttk.Label(self.root, text="Enter a Task")
        self.labelTask.pack()
        self.taskInput = ttk.Entry(self.root)
        self.taskInput.pack()
        self.addButton = ttk.Button(self.root, text="Add Task", command=self.addTask)
        self.addButton.pack()
        self.editButton = ttk.Button(self.root, text="Edit Task", command=self.editTask)
        self.editButton.pack()
        self.deleteButton = ttk.Button(self.root, text="Delete Task", command=self.deleteTask)
        self.deleteButton.pack()
        self.comboboxLabel = ttk.Label(self.root, text="Update Status")
        self.comboboxLabel.pack()
        self.combobox = ttk.Combobox(self.root, values=["In Progress", "Completed"])
        self.combobox.current(0)
        self.combobox.pack()
        self.tree = ttk.Treeview(self.root, columns=("Task No.", "Task Description", "Task Status"),show="headings")
        self.tree.heading("Task No.", text="Task No.")
        self.tree.heading("Task Description", text="Task Description")
        self.tree.heading("Task Status", text="Task Status")
        self.tree.pack()
   
         
      
    def deleteTask(self):
        selectedItem = self.tree.selection()
        if selectedItem:
            self.tree.delete(selectedItem[0])
        else:
            messagebox.showerror("Error", "No Task Selected")
            
    def editTask(self):
        selectedItem = self.tree.selection()
        if selectedItem:
            self.tree.item(selectedItem[0], values=(self.taskManagerCounter,self.taskInput.get(), self.combobox.get()))
        else:
            messagebox.showerror("Error", "No Task Selected")
           
    def addTask(self): 
        
        # it should be asc increment    
        self.taskManagerCounter += 1 
        self.tree.insert("", "end", text = self.taskManagerCounter, values = (self.taskManagerCounter, self.taskInput.get(), "Pending"))
    def calculateGrade(self):
        sum = 0
        for i in range(len(self.ArrayGrade)):
            sum += int(self.ArrayGrade[i].get())
        messagebox.showinfo("Average", "The Average Grade Is " + str(sum / len(self.ArrayGrade)))
      
        
    def submit(self):
        username = self.textbox_userName.get()
        password = self.textbox_password.get()
        if username == "admin" and password == "admin":
            messagebox.showinfo("Success", "Login Successful")
        else:
            messagebox.showerror("Error", "Invalid Credentials")
        
    def reset(self):
        self.counter = 0
        self.number.config(text=self.counter)
    def decrement(self):
        self.counter -= 1
        self.number.config(text=self.counter)
    def increment(self):
        self.counter += 1
        self.number.config(text=self.counter)
   
    def run(self):
        self.root.mainloop()
        

GUI = Iksirsays()
GUI.run()