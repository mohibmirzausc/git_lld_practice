# Simple Library Management System

## Problem Statement

Design a Simple Library Management System to keep track of books, patrons, and checkouts. The system should handle:

- **Books**: Each book has a title, author, and a unique identifier (ISBN).
- **Patrons**: Each patron has a name, unique ID, and a list of books they’ve checked out.
- **Checkout System**: Patrons can borrow and return books. The system ensures:
  - Each book can be checked out by only one patron at a time.
  - A patron can check out multiple books but must return them within a given period (e.g., 14 days).
- **Due Dates and Fees**: If a book is returned late, the patron is charged a fee for each overdue day.
- **Reports**:
  - List all books checked out by a patron.
  - List overdue books with their respective fees.

## Tasks

- Implement classes for Book, Patron, and Library.
- Implement methods for borrowing and returning books.
- Handle overdue fees and report generation.
- Design the system to be easily extendable in the future (e.g., adding a reservation system, digital library, etc.).

## Requirements

- Basic functionality for checking in and checking out books.
- Due date system and calculation of overdue fees.
- Basic reports for:
  - All books checked out by a patron.
  - Books overdue and the corresponding fees.
- Design should allow for easy future extensions.

## Constraints

- The library can hold up to 100 books and patrons.
- Book titles and patron names are strings; IDs are integers.
- Books and patrons are identified by unique IDs.