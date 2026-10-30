class ManagedFile:
    def __init__(self, filename):
        self.filename = filename
    
    def __enter__(self):
        print(f"[1] Opening file {self.filename}\n")
        self.file = open(self.filename, "w")
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"[3] Automatically closed file {self.filename}\n")
    
if __name__ == "__main__":
    with ManagedFile("output.txt") as file:
        print("[2] Writing text inside the file.....")
        file.write("Hello Kalibutan! Safe successfully")

    print("-" * 40)
    print("Context Manager finished")
    
    print("[4] Reading contents from output.txt")
    with open("output.txt", "r") as file:
        content = file.read()
        print(f"File Content: {content}")
        
        
    
   
        
    
    
   