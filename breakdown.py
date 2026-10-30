import fileManage
from tkinter import *
from tkinter import ttk, messagebox
import json

HISTORY_FILE = "calculator.json"

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("My Application")
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack()
        self.Label("Enter The First Number")
        self.firstNumber = self.TextBox()
        self.Label("Select An Operator (+, -, x, /)")
        self.operator = self.Combobox(['+', '-', 'x', '/'])
        self.operator.current(0)
        self.Label("Enter The Second Number")
        self.secondNumber = self.TextBox()
        self.Button("SUBMIT", self.calculate)
        self.resultLabel = self.Label("")
        self.Button("HISTORY", self.history)
        self.historyList = self.Label("")
        self.historyList.config(wraplength=280)
        self.historyEntries = self.loadHistory()
        self.Table()
        
    def Table(self):
        table = ttk.Treeview(self.frame, columns=["First Number", "Operator", "Second Number", "Result"], show="headings")
        table.heading("First Number", text="First Number")
        table.heading("Operator", text="Operator")
        table.heading("Second Number", text="Second Number")
        table.heading("Result", text="Result")
        
        for i in self.historyEntries:
            if isinstance(i, dict):
                table.insert("", "end", values=(i.get("a"), i.get("operator"), i.get("b"), i.get("result")))
            else:
                # Lumang format: "7 + 3 = 10"
                parts = str(i).split()
                table.insert("", "end", values=(parts[0], parts[1], parts[2], parts[4]))
        
        table.pack()
        return table

    def calculate(self):
        firstNumber = self.firstNumber.get()
        secondNumber = self.secondNumber.get()
        operator = self.operator.get()
        try:
            a = int(firstNumber)
            b = int(secondNumber)
        except ValueError:
            self.showErrorDialog("Error", "Please Enter Valid Whole Numbers")
            return
        if operator == "+":
            result = a + b
            self.showInfoDialog("Result", "The Sum Of " + firstNumber + " and " + secondNumber + " is " + str(result))
            self.resultLabel.config(text=f"{a} + {b} = {result}")
        elif operator == "-":
            result = a - b
            self.showInfoDialog("Result", "The Difference Of " + firstNumber + " and " + secondNumber + " is " + str(result))
            self.resultLabel.config(text=f"{a} - {b} = {result}")
        elif operator == "x":
            result = a * b
            self.showInfoDialog("Result", "The Product Of " + firstNumber + " and " + secondNumber + " is " + str(result))
            self.resultLabel.config(text=f"{a} x {b} = {result}")
        elif operator == "/":
            if b == 0:
                self.showErrorDialog("Error", "Cannot Divide By Zero")
                return
            result = a / b
            self.showInfoDialog("Result", "The Division Of " + firstNumber + " and " + secondNumber + " is " + str(result))
            self.resultLabel.config(text=f"{a} / {b} = {result}")
        else:
            self.showErrorDialog("Error", "Invalid Operator")
            return
        entry = {"a": a, "operator": operator, "b": b, "result": result}
        self.historyEntries.append(entry)
        self.saveHistory()
    
    def history(self):
        self.historyEntries = self.loadHistory()
        if not self.historyEntries:
            self.historyList.config(text="No History Yet")
            return
        self.historyList.config(text="\n".join(
            f'{e["a"]} {e["operator"]} {e["b"]} = {e["result"]}' if isinstance(e, dict) else str(e)
            for e in self.historyEntries
        ))

    def loadHistory(self):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def saveHistory(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(self.historyEntries, file, indent=4)
        
       
    
    def run(self):
        self.root.mainloop()
        
    def Label(self, text):
        label = ttk.Label(self.frame, text = text)
        label.pack()
        return label
    def Button(self,text,command):
        button = ttk.Button(self.frame, text=text, command=command)
        button.pack()
        return button
    def TextBox(self):
        textbox = ttk.Entry(self.frame)
        textbox.pack()
        return textbox
    def Combobox(self,values):
        combobox = ttk.Combobox(self.frame, values=values)
        combobox.pack()
        return combobox
    
    def showInfoDialog(self,title,text):
        messagebox.showinfo(title,text)
        
    def showErrorDialog(self,title,text):
        messagebox.showerror(title,text)
        
    def showWarningDialog(self,title,text):
        messagebox.showwarning(title,text)
    
        



if __name__ == "__main__":
    app = GUI()
    app.run()
    
    