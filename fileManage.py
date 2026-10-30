import os
class ManagedFile:
    def __init__(self, fileName, mode):
        self.filename = fileName
        self.mode = mode
        self.file = None
        
    def __enter__(self):
        print(f"\n[SYSTEM] Opening {self.filename} in {self.mode} mode ...")
        self.file = open(self.filename, self.mode)
        return self.file
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"[SYSTEM] {self.filename} in {self.mode} safely closed")
        return False

class FileManaged:
    def __init__(self, fileName):
        self.filename = fileName
    def writeFile(self, fileName):
        if os.path.exists(fileName.lower()):
            print(f"The File is Already Existing {fileName.lower()}")
            return
        with ManagedFile(fileName, "w") as file:   
            content = input("Enter text: ").strip()
            file.write(content + "\n")
    def appendFile(self, fileName):
        with ManagedFile(fileName, "a") as file:   
            content = input("Enter text: ").strip()
            file.write(content + "\n")
    def readFile(self, fileName):
        find = input("Enter a filename to read with it: ").strip()
        if os.path.exists(find):
            with ManagedFile(find, "r") as file:   
                content = file.read()
                print(content)    
        else:
            print(f"\n[ERROR] {find} does not exist yet. Write Something first")

    def deleteFile(self, fileName):
        if not os.path.exists(fileName):
            print(f"\n[ERROR] {fileName} does not exist yet. Write Something first")
            return
        confirm = input(f"Are you sure you want to delete this file {fileName}? (y/n): ").strip().lower()
        if confirm != "y":
            print("File not deleted")
            return
        os.remove(fileName)
        print(f"\n[SUCCESSFULLY] Deleted {self.filename}")
    
def run():
    fileName = input("Enter a Filename to want to work with (e.g.txt my_notes.txt): ").strip()
    FM = FileManaged(fileName)
    while True:
        print("\n[SYSTEM]\n1. Write Text (overwrite existing file)\n2. Append Text (add to existing file)\n3. Read file contents\n4. Delete the file\n5. EXIT")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            FM.writeFile(fileName)
        elif choice == "2":
            FM.appendFile(fileName)
        elif choice == "3":
            FM.readFile(fileName)
        elif choice == "4":
            FM.deleteFile(fileName)
        elif choice == "5":
            break
        else:
            print("Invalid choice") 
            
if __name__ == "__main__":
    run()