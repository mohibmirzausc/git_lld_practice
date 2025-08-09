from book import Book
from patron import Patron
from library import Library
import unittest

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        book_isbn = self.library.create_book("The Invention of Hugo Cabret", "Brian Selznick")
        self.hugo = self.library.get_book(book_isbn)
        patron_uuid = self.library.create_patron("Steve")
        self.steve = self.library.get_patron(patron_uuid)


    def test_create_book(self):
        self.assertEqual(self.hugo.title, "The Invention of Hugo Cabret")
        self.assertEqual(self.hugo.author, "Brian Selznick")
        self.assertEqual(self.hugo.checked_out, False)
        self.assertEqual(self.hugo.borrower_uid, None)
        self.assertEqual(self.hugo.due_date, None)

    def test_create_patron(self):
        self.assertEqual(self.steve.name, "Steve")
        self.assertTrue(len(self.steve.books) == 0)

    def test_patron_borrows_book(self):
        self.assertTrue(self.steve.borrow(self.hugo))
        self.assertTrue(self.hugo.checked_out)
        self.assertEqual(self.steve.uuid, self.hugo.borrower_uid)

    def test_patron_returns_book_direct(self):
        self.steve.borrow(self.hugo)
        self.assertFalse(self.hugo.is_overdue())
        self.assertTrue(self.steve.return_book(self.hugo))
        self.assertFalse(self.hugo in self.steve.books)
        self.assertFalse(self.hugo.checked_out)

    def test_patron_returns_book(self):
        return True

    



if __name__ == '__main__':
    unittest.main(verbosity=2)
