class Student:
    def __init__(self, name, age, course):
        self.age = age
        self.name = name
        self.course = course
        
class StudentManagementSystem:
    def __init__(self):
        self.students = []
    
    def add_student(self, student):
        
        self.students.append(student)
        print(f"Student {student.name} added successfully")
    
    def remove_student(self, student):
        self.students.remove(student)
        print(f"Student {student.name} removed successfully")
    
    def display_students(self):
        for student in self.students:
            print(student)
    def addQuiz(self):
        name = input("Enter the name of the student: ")
        for student in self.students:
            if student.name == name:
                quiz = int(input(f"Enter quiz for {student.name}: "))
                student.quiz.append(quiz)
                print(f"Quiz added successfully for {student.name}")
                break
            else:
                print(f"Student {name} not found")


if __name__ == "__main__":
  
    sms = StudentManagementSystem()
    
    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
           name = input("Enter the name of the student: ")
           age = int(input("Enter the age of the student: "))
           course = input("Enter the course of the student: ")
           student = Student(name, age, course)
           sms.add_student(student)
        elif choice == "2":
            sms.display_students()
        elif choice == "3":
            sms.addQuiz()
        elif choice == "4":
            name = input("Enter the name of the student to remove: ")
            for student in sms.students:
                if student.name == name:
                    sms.remove_student(student)
                    break
                else:
                    print(f"Student {name} not found")
        elif choice == "5":
            break
        else:
            print("Invalid choice")
    