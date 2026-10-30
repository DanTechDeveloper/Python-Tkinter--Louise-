from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("My Application")
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack()
        
        self.labelExample = self.create_label("Hello World", 0,0)
        self.textboxExample = self.create_textbox(1,0)
        self.comboboxExample = self.create_combobox(["Option 1", "Option 2", "Option 3"], 2,0)
        self.comboboxExample.current(0)
        self.buttonExample = self.create_button("Click Me", 3,0, self.on_click)
    
    
    
    def on_click(self):
        messagebox.showinfo("Button Clicked", "You clicked the button!")
    
    def create_label(self, text, row, column):
        label = ttk.Label(self.frame, text=text)
        label.grid(row=row,column=column)
        return label    
    
    def create_button(self, text, row, column,  command):
        button = ttk.Button(self.frame, text=text, command=command)
        button.grid(row=row, column=column)
        return button
    
    def create_textbox(self, row, column):
        textbox = ttk.Entry(self.frame)
        textbox.grid(row=row, column=column)
        return textbox
    
    def create_combobox(self, values, row, column):
        combobox = ttk.Combobox(self.frame, values=values)
        combobox.grid(row=row, column=column)
        return combobox
    
    def run(self):
        self.root.mainloop()
        
        
        
        
gui = GUI()
gui.run()
    