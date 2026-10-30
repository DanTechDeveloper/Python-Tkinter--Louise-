import os
class ManagedFile:
    def __init__(self, filename, mode="w"):
        self.filename = filename
        self.mode = mode
    def __enter__(self):
        print(f"[SYSTEM] OPENING {self.filename} in {self.mode} mode ...")
        self.file = open(self.filename, self.mode)
        return self.file
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"[SYSTEM] {self.filename} in {self.mode} safely closed")    


if __name__ == "__main__":
    fileName = input("Enter a Filename to want to work with (e.g.txt my_notes.txt): ").strip()
    
    print("-" * 50)
    
    print("[1]. Write Text (overwrite existing file)")
    print("[2]. Append Text (add to existing file)")
    print("[3]. Read file contents")
    print("[4]. EXIT")
    
    print("-" * 50)
    while True:
        choice = input("Enter your choice: 1-4: ").strip()
        if (choice == "1"):
            text = input("Enter the text you want to write: ").strip()
            with ManagedFile(fileName, "w") as file:
                file.write(text + "\n")
            print("\n[SUCCESSFULLY] written!")
        elif (choice == "2"):
            text = input("Enter the text you want to append: ").strip()
            with ManagedFile(fileName, "a") as file:
                file.write(text + "\n")
            print("\n[SUCCESSFULLY] appended!")
        elif (choice == "3"):
            if not os.path.exists(fileName):
                print(f"\n[ERROR] {fileName} does not exist yet. Write Something first")
                continue
                        
            with ManagedFile(fileName, "r") as file:
                content = file.read()
                print("\n[FILE CONTENT]")
                print(content if content else "The file is empty!")
                
        elif (choice == "4"):
            print("\n[EXITING] Thank You for using this program!")
            break
        else:
            print("\n[ERROR] Invalid choice. Please try again.") 
        
    
    
        