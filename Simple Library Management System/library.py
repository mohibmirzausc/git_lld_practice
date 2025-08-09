import uuid
from patron import Patron
from book import Book

class Library:
    def __init__(self):
        self.books = {}
        self.patrons = {}

    def create_patron(self, name):
        patron = Patron(name)
        self.patrons[patron.uuid] = patron
        print("Your patron has been added. ID: ", patron.uuid)
        return patron.uuid
    
    def create_book(self, title, author):
        book = Book(title, author)
        self.books[book.isbn] = Book(title, author)
        print("Your book has been added. ISBN: ", book.isbn)
        return book.isbn

    def get_patron(self, uuid):
        return self.patrons.get(uuid, None)
    
    def get_book(self, isbn):
        return self.books.get(isbn, None)

    def patron_borrows_book(patron_uuid, book_isbn):
        patron = self.get_patrong(patron_uuid)
        book = self.get_book(get_book(book_isbn))
        if not patron:
            print("Patron doesn't exist! Cannot execute borrow!")
            return False

        if not book:
            print("Book doesn't exist! Cannot execute borrow!")
            return False

        return patron.borrow(book)



    
        


