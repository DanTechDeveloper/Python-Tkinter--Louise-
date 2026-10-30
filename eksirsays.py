from tkinter import ttk
from tkinter import * 
from tkinter import messagebox

class Esmerenghoy:
    def __init__(self):
        self.root = Tk()
        self.root.title("BEMBANGAN SYSTEM BUY A GIRL")
        
        self.label = ttk.Label(self.root, text="BUY A GIRL")
        self.label.pack()
        
        self.Userinput = ttk.Entry(self.root)
        self.Userinput.pack()
        
        self.labelCombobox = ttk.Label(self.root, text="Listahan Ng Year level")
        self.labelCombobox.pack()
        
        self.combobox = ttk.Combobox(self.root, values=("1st Year", "2nd Year", "3rd Year", "4th Year"))
        self.combobox.pack()
        self.combobox.current(0)
        
        self.button = ttk.Button(self.root, text="PINDUTIN MOKO", command=self.pindutinMoko)
        self.button.pack()
    
    def pindutinMoko(self):
        valueKo = self.Userinput.get()
        messagebox.showinfo("MENSAHE", "Hi: " + valueKo)    
        
    def run(self):
        self.root.mainloop()
        
        
nabembang = Esmerenghoy()
nabembang.run()        