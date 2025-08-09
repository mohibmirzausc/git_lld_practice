import uuid
from book import Book

class Patron:
    def __init__(self, name):
        self.name = name
        self.books = set()
        self.uuid = uuid.uuid4()

    def borrow(self, book: Book):
        self.books.add(book)
        return book.borrow(self.uuid)

    def return_book(self, book: Book):
        if book not in self.books:
            return False
        
        self.books.remove(book)

        return book.return_book()