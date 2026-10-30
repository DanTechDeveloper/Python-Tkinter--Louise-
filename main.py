students = {};
def addStudent():
    studentId = input("Enter student ID: ")
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    grade = input("Enter student grade: ")
    email = input("Enter student email: ")
    address = input("Enter student address: ")
    contactNumber = input("Enter student contact number");
    guardianName = input("Enter guardian name")
    
    if studentId in students:
        print("Student ID already exists.")
    else:
        students[studentId] = {"name": name, "age": age, "grade": grade, "email": email, "address": address, "contactNumber": contactNumber, "guardianName": guardianName}
        print("Student added successfully.")
        tryAgain = ""
        while tryAgain.lower() != "y" and tryAgain.lower() != "n":
            tryAgain = input("Do you want to add another student? (y/n): ").strip()
            if tryAgain.lower() == "y":
                addStudent()
            elif tryAgain.lower() == "n":
                break
            else:
                print("Invalid input. Please try again.")
    
def viewStudent():
    if len(students) == 0:
        print("No students found.")
        return
    
    for studentId in students:
        print("Student ID: ", studentId)    
        print("Name: ", students[studentId]["name"])
        print("Age: ", students[studentId]["age"])
        print("Grade: ", students[studentId]["grade"])
        print("Email: ", students[studentId]["email"])
        print("Address: ", students[studentId]["address"])
        print("Contact Number: ", students[studentId]["contactNumber"])
        print("Guardian Name: ", students[studentId]["guardianName"])
        
def updateStudent():
    studentId = input("Enter student ID to update: ").strip()
    if studentId not in students:
        print("Student ID not found.")
        return
    else:
        newName = input("Enter a new name: ").strip();
        newAge = input("Enter a new age: ").strip();
        newGrade = input("Enter a new grade: ").strip();
        newEmail = input("Enter a new email: ").strip();
        newAddress = input("Enter a new address: ").strip();
        newContactNumber = input("Enter a new contact number").strip();
        newGuardianName = input("Enter a new guardian name").strip();
        students[studentId] = {"name": newName, "age": newAge, "grade": newGrade, "email": newEmail, "address": newAddress, "contactNumber": newContactNumber, "guardianName": newGuardianName}
        print("Student updated successfully.")
    
def deleteStudent():
    choice = 0;
    while choice != 3:
        print("1. Delete Student By Id")
        print("2. Delete Student By Name")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
           deleteStudentByType("Id");
        elif choice == '2':
            deleteStudentByType("Name")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def deleteStudentByType(type):
    if type == 'Id':
        studentId = input("Enter student ID to delete: ").strip()
        if studentId not in students:
            print("Student ID not found.")
            return
        else:
            del students[studentId]
        print("Student deleted successfully.")
    elif type == "Name":
        studentName = input("Enter student Name to delete: ").strip()
        foundIds = []
        for sid in students:
            if students[sid]["name"].lower() == studentName.lower():
                foundIds.append(sid)
        if len(foundIds) == 0:
            print("Student Name not found.")
            return
        for sid in foundIds:
            del students[sid]
        print(f"Deleted {len(foundIds)} student(s) named '{studentName}'.")
        
def searchStudent():
    choice = 0;
    while choice != 3:
        print("1. Search Student By Id")
        print("2. Search Student By Name")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
           searchStudentByType("Id");
        elif choice == '2':
            searchStudentByType("Name")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
        
def searchStudentByType(type):
    if type == 'Id':
        studentId = input("Enter student ID to search: ").strip()
        if studentId not in students:
            print("Student ID not found.")
            return
        else:
            print("Student ID: ", studentId)
            print("Name: ", students[studentId]["name"])
            print("Age: ", students[studentId]["age"])
            print("Grade: ", students[studentId]["grade"])
            print("Email: ", students[studentId]["email"])
            print("Address: ", students[studentId]["address"])
    elif type == "Name":
        studentName = input("Enter student Name to search: ").strip()
        found = False
        for sid in students:
            if students[sid]["name"].lower() == studentName.lower():
                print("Student ID: ", sid)
                print("Name: ", students[sid]["name"])
                print("Age: ", students[sid]["age"])
                print("Grade: ", students[sid]["grade"])
                print("Email: ", students[sid]["email"])
                print("Address: ", students[sid]["address"])
                found = True
        if not found:
            print("Student Name not found.")
                
def main():
    choice = 0
    while choice != 6:
        print("1. Add Sutudent")
        print("2. View Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search Student")      
        print("6. Exit")
        choice = input("Enter your choice: (1-6) ").strip()
        if choice == '1':
            addStudent()
        elif choice == '2':
            viewStudent()
        elif choice == '3':
            updateStudent()
        elif choice == '4':
            deleteStudent()
        elif choice == '5':
            searchStudent()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
    

    
if (__name__ == '__main__'):    
    main()