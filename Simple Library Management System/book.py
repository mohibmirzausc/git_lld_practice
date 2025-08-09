import uuid
from datetime import timedelta, datetime

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.isbn = uuid.uuid4()
        self.checked_out = False
        self.borrower_uid = None
        self.due_date = None

    def borrow(self, patron_uuid):
        if self.checked_out:
            print(f"[ERROR] Patron {patron_uuid} tried to check out checked out book {self.isbn}")
            return False

        self.borrower_uid = patron_uuid
        self.checked_out = True
        due_date = datetime.today() + timedelta(days=14)
        self.due_date = due_date.strftime("%Y-%m-%d")

        return True

    def is_overdue(self):
        current_date = datetime.today()
        overdue_days = (current_date - datetime.strptime(self.due_date, "%Y-%m-%d")).days
        return overdue_days > 14

    def return_book(self):
        if not self.checked_out:
            print(f"[ERROR] This book was not checked out.")
            return False
        self.checked_out = False
        self.borrower_uid = None
        


        if self.is_overdue():
            fee = 0.5 * overdue_days
            print("Book is overdue! You owe $", fee, " to the library!")
        else:
            print("Book is not overdue. Return was successful.")
        
        self.due_date = None
        return True
        


    