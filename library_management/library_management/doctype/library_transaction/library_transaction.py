# Copyright (c) 2025, LuxTech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            # set the book status to be Issued
            books = frappe.get_doc("Books", self.books)
            books.status = "Issued"
            book_name = self.books
            library_member = self.library_member
            
            # verify book_name field
            if not book_name:
                frappe.throw(_("Please select a Book for this transaction."))
                
            # Check if the member has already borrowed the same book
            existing_transaction = frappe.db.exists({
                "doctype": "Library Transaction",
                "type": "Issue",
                "library_member": library_member,
                "books": book_name,
                "docstatus": 1  # Assuming docstatus 1 represents 'Submitted' and active transactions
            })

            if existing_transaction:
                frappe.throw(_("Library Member {0} has already borrowed the book {1} and has not returned it yet.")
                            .format(library_member, book_name))
            
            # Decrement available copies if there is at least one available
            if books.available_copies <= 0:
                frappe.throw("No copies available for this book")
            books.available_copies -= 1
            books.save()

        elif self.type == "Return":
            self.validate_return()
            # set the book status to be Available
            books = frappe.get_doc("Books", self.books)
            books.status = "Available"
            books.save()

    def validate_issue(self):
        self.validate_membership()
        books = frappe.get_doc("Books", self.books)
        # book cannot be issued if it is already issued
        if books.available_copies <= 0:
            frappe.throw("No copies available for this book, All copies issued out")

    def validate_return(self):
        books = frappe.get_doc("Books", self.books)
        # article cannot be returned if it is not issued first
        if books.status == "Available":
            frappe.throw("Books cannot be returned without being issued first")

    # Limiting number of books library member can borrow
    def validate_maximum_limit(self):
        max_books_allowed = 3  # Maximum books allowed per member
        # Count the number of active borrowings for this library member
        borrowed_books = frappe.db.count("Library Transaction", {
            "library_member": self.library_member,
            "docstatus": 1,  # Only count submitted transactions
            "return_date": ["=", None]  # The book has not been returned
        })

        if borrowed_books >= max_books_allowed:
            frappe.throw(_("This member has already borrowed the maximum allowed books ({0}). They must return a book before borrowing another.").format(max_books_allowed))
            
    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.issue_date),
                "to_date": (">", self.issue_date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
