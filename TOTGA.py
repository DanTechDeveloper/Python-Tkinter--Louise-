class ManagedFile:
    def __init__(self, filename, mode="w"):
        self.filename = filename
        self.mode = mode
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    

if __name__ == "__main__":
    with ManagedFile("output.txt", "w") as file:
        file.write("Hello Kalibutan! Safe successfully")
    print("File closed automatically")
    
    with ManagedFile("output.txt", "r") as file:
        content = file.read()
        print(content)
    print("File closed automatically") 