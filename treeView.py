from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class TreeView:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tree View Introduction")
        self.create_label("Search Bar")
        self.searchBar = self.create_userInput()
        self.create_button("Search", self.search)
        
        self.studentID = self.create_label("Enter Student-ID")
        self.studentIdTextBox = self.create_userInput()
        
        self.studentName = self.create_label("Enter Student Name")
        self.studentNameTextBox = self.create_userInput()

        self.studentCourse = self.create_label("Enter Student Course")
        self.studentCourseTextBox = self.create_userInput()

        self.studentYear = self.create_label("Enter Student Year")
        self.studentYearTextBox = self.create_userInput()
        
        self.addButton = self.create_button("Add", self.add)
        self.updateButton = self.create_button("Update", self.update)
        self.deleteButton = self.create_button("Delete", self.delete)
        
        self.create_label("Table")
        self.dataTable = self.create_table(["Student-ID", "Student Name", "Student Course", "Student Year"])
        self.tableData = []
        for i in self.dataTable.get_children():
            self.tableData.append(self.dataTable.item(i, "values"))
            
    def delete(self):
        selectedRow = self.dataTable.selection()
        
        if not selectedRow:
            self.messageInfo("Error", "Please select a row to delete")
            return
        
        if (self.messageYesOrNo("Deleting Data Row?", "Are you sure you want to delete this student information")):
            oldData = self.dataTable.item(selectedRow[0], "values")
            self.dataTable.delete(selectedRow)
            for i in range(len(self.tableData)):
                if self.tableData[i] == oldData:
                    del self.tableData[i]
                    break
            self.messageInfo("Success", "Student information deleted successfully")
        else:
            self.messageInfo("Cancelled", "Student information not deleted")
            
    def add(self):
        studentID = self.studentIdTextBox.get()
        studentName = self.studentNameTextBox.get()
        studentCourse = self.studentCourseTextBox.get()
        studentYear = self.studentYearTextBox.get()
        
        if studentID != "" and studentName != "" and studentCourse != "" and studentYear != "":
            if (self.messageYesOrNo("Confirm", "Are you sure you want to add this student?")):
                self.dataTable.insert("", "end", values=(studentID, studentName, studentCourse, studentYear))
                self.tableData.append((studentID, studentName, studentCourse, studentYear))
                print(self.tableData)
                self.messageInfo("Success", "Student added successfully")
            else:
                self.messageInfo("Cancelled", "Student not added")
        else:
            self.messageInfo("Error", "Please fill in all the fields")
        
        
    def update(self):
        selectedRow = self.dataTable.selection()
        if not selectedRow:
            self.messageInfo("Error", "Please select a row to update")
            return

        studentID = self.studentIdTextBox.get()
        studentName = self.studentNameTextBox.get()
        studentCourse = self.studentCourseTextBox.get()
        studentYear = self.studentYearTextBox.get()
        
        if studentID != "" and studentName != "" and studentCourse != "" and studentYear != "":
            if (self.messageYesOrNo("Confirm", "Are you sure you want to update this student?")):
                oldDataSelection = self.dataTable.item(selectedRow[0], "values")
                self.dataTable.item(selectedRow[0], values=(studentID, studentName, studentCourse, studentYear))
                if selectedRow:
                    for i in range(len(self.tableData)):
                        if self.tableData[i] == oldDataSelection:
                            self.tableData[i] = (studentID, studentName, studentCourse, studentYear)
                            break
                    
                    
                
                self.messageInfo("Success", "Student updated successfully")
            else:
                self.messageInfo("Cancelled", "Student not updated")
        else:
            self.messageInfo("Error", "Please fill in all the fields")
        
        
    def search(self):
        searchResult = self.searchBar.get()
        found = False
        for i in self.dataTable.get_children():
            self.dataTable.delete(i)
            
        for i in self.tableData:
            if searchResult.lower() == i[1].lower() or searchResult.lower() == i[2].lower() or searchResult.lower() == i[3].lower():
                self.dataTable.insert("","end", values=i)
                found = True
            else:
                continue
            
        if (found):
            self.messageInfo("Success", "Student Found!")
        else:
            self.messageInfo("Not Found", "Student Not Found!") 
           
    
      
    def create_button(self, text, command):
        button = ttk.Button(self.root, text=text, command=command)
        button.pack()
        return button
    
    def create_label(self, text):
        label = ttk.Label(self.root, text=text)
        label.pack()
        return label
    
    def create_userInput(self):
        userInput = ttk.Entry(self.root)
        userInput.pack()
        return userInput
    
    def messageInfo(self,title,message):
        messagebox.showinfo(title,message)
        
    def messageYesOrNo(self,title,message):
        return messagebox.askyesno(title,message)
        
    
    def create_table(self, column):
        self.table = ttk.Treeview(self.root, columns=column, show="headings")
        for i in range(len(column)):
            self.table.heading(column[i], text=column[i])
        self.table.pack()
        return self.table


        
   
    
      
    def run(self):
        self.root.mainloop()
        
        
        
        
treeView = TreeView()
treeView.run()
        
    