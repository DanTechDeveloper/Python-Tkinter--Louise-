
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.checkedOut = False

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}"
    
    def check_out(self):
        if not self.checkedOut:
            self.checkedOut = True
            return True
        return False

    def return_book(self):
        if self.checkedOut:
            self.checkedOut = False
            return True
        return False

    def __str__(self):
        status = "Checked Out" if self.checkedOut else "Available"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - [{status}]"
    

class Library:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def check_out_book(self, isbn):
        if len(self.books) == 0:
            print("No books found.")
            return
        for book in self.books:
            if book.isbn == isbn:
                if book.check_out():
                    print("Book checked out successfully.")
                else:
                    print("Book is already checked out.")
                return
            return
        print("Book not found.")

    def return_book(self, isbn):
        if len(self.books) == 0:
            print("No books found.")
            return
        for book in self.books:
            if book.isbn == isbn:
                book.return_book()
                print("Book returned successfully.")
                return
        print("Book not found.")

    def search_book(self,isbn):
        
        for book in self.books:
            if book.isbn == isbn:
                return book
            elif book.isbn == isbn:
                return "Book is already checked out."
        return "Book not found."
    
    def viewBooks(self):
        if len(self.books) == 0:
            print("No books found.")
            return
        for book in self.books:
            print(book)
            
    def deleteBook(self,isbn):
        if len(self.books) == 0:
            print("No books found.")
            return
        for book in self.books:
            if book.isbn == isbn:
                del self.books[isbn]
                print("Book deleted successfully.")
                return
        print("Book not found.")
    
    
if __name__ == "__main__":
    library = Library()
    
    library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", "1234"))
    library.add_book(Book("To Kill a Mockingbird", "Harper Lee", "5678"))
    library.add_book(Book("1984", "George Orwell", "978-0451524935"))
    library.add_book(Book("The Catcher in the Rye", "J.D. Salinger", "9101112"))
    library.add_book(Book("The Hobbit", "J.R.R. Tolkien", "13141516"))
    library.add_book(Book("The Lord of the Rings", "J.R.R. Tolkien", "17181920"))
    
   
    
    choice = "0";
    while choice != 6:
            print("1. Add Book")
            print("2. View Book")
            print("3. Delete Book")
            print("4. Search Book")
            print("5. Checkout Book");
            print("6. Return Book");
            print("7. Exit");
            choice = input("Enter your choice: 1-7: ").strip()

            if choice == '1':
                title = input("Enter book title: ").strip()
                author = input("Enter book author: ").strip()
                isbn = input("Enter book ISBN: ").strip()
                library.add_book(Book(title, author, isbn))
            elif choice == '2':
                library.viewBooks()
            elif choice == '3':
                isbn = input("Enter book ISBN to delete: ").strip()
                library.deleteBook(isbn)
            elif choice == '4':
                search = input("Search Book By ISBN: ").strip()
                book = library.search_book(search)
                if book:
                   print(book)
                   if not book.checkedOut:
                       checkout = input("Do you want to checkout this book? (y/n): ").strip()
                       if checkout.lower() == 'y':
                           library.check_out_book(search)
                       else:
                           print("Exit")
                   else:
                       print("Book is already checked out.")
                else:
                    print("Book not found.")
            elif choice == '5':
                isbn = input("Enter book ISBN to checkout: ").strip()
                library.check_out_book(isbn)
            elif choice == '6':
                isbn = input("Enter book ISBN to return: ").strip()
                library.return_book(isbn)
            elif choice == '7':
                break
            
            else:
                print("Invalid choice. Please try again.")

            
