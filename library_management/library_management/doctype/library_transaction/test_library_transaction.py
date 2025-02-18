# Copyright (c) 2025, LuxTech and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase
import unittest
from .import library_transaction

from frappe.exceptions import ValidationError


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
# IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
# 
# 
# class UnitTestLibraryTransaction(UnitTestCase):
	# """
	# Unit tests for LibraryTransaction.
	# Use this class for testing individual functions and methods.
	# """
# 
	# pass
# 
# 
# class IntegrationTestLibraryTransaction(IntegrationTestCase):
	# """
	# Integration tests for LibraryTransaction.
	# Use this class for testing interactions between multiple components.
	# """
# 
	# pass
# 




class TestLibraryTransaction(unittest.TestCase):
    def setUp(self):
        # Setup method to create necessary test data before each test
        # Clear any existing Library Transactions for test isolation
        frappe.db.sql("DELETE FROM `tabLibrary Transaction` WHERE type='Issue'")
        frappe.db.sql("DELETE FROM `tabBooks` WHERE title='Test Book'")
        frappe.db.sql("DELETE FROM `tabLibrary Member` WHERE library_member_name='Test Member'")

        self.test_book = frappe.get_doc({
            "doctype": "Books",
            "title": "Test Book",
            "total_number_of_copies": 2,
            "available_copies": 2
        }).insert()

        self.test_member = frappe.get_doc({
            "doctype": "Library Member",
            "library_member_name": "Test Member"
        }).insert()

    def tearDown(self):
        # Teardown method to clean up test data after each test
        frappe.db.rollback() # Rollback any database changes made during the test

    def test_duplicate_book_borrowing_prevented(self):
        # Test case: Check if borrowing the same book twice is prevented

        # 1. Create an existing 'Issue' transaction for the test member and book
        existing_transaction = frappe.get_doc({
            "doctype": "Library Transaction",
            "type": "Issue",
            "books": "Test Book",  # Use book title, assuming your 'books' field is linked by title
            "library_member": "Test Member", # Use member name, assuming 'library_member' is linked by name
            "issue_date": frappe.utils.today(),
            "return_date": frappe.utils.add_days(frappe.utils.today(), 5),
        }).insert()
        existing_transaction.submit() # Submit the existing transaction to make it active

        # 2. Attempt to create a new 'Issue' transaction for the same member and book
        new_transaction = frappe.new_doc("Library Transaction")
        new_transaction.type = "Issue"
        new_transaction.books = "Test Book" # Use book title
        new_transaction.library_member = "Test Member" # Use member name
        new_transaction.issue_date = frappe.utils.today()
        new_transaction.return_date = frappe.utils.add_days(frappe.utils.today(), 5)

        # 3. Assert that submitting the new transaction raises a ValidationError
        with self.assertRaises(ValidationError) as cm:
            new_transaction.submit()

        # 4. Optionally, check if the error message is as expected
        self.assertTrue("Library Member Test Member has already borrowed the book Test Book and has not returned it yet." in str(cm.exception))

    def test_duplicate_book_borrowing_allowed_different_member(self):
        # Test case: Borrowing same book is allowed for a different member

        # 1. Create an existing 'Issue' transaction for a *different* member and the test book
        different_member = frappe.get_doc({
            "doctype": "Library Member",
            "library_member_name": "Different Member"
        }).insert()
        existing_transaction = frappe.get_doc({
            "doctype": "Library Transaction",
            "type": "Issue",
            "books": "Test Book",
            "library_member": "Different Member", # Different member here
            "issue_date": frappe.utils.today(),
            "return_date": frappe.utils.add_days(frappe.utils.today(), 5),
        }).insert()
        existing_transaction.submit()

        # 2. Attempt to create a new 'Issue' transaction for the *test member* and the same book
        new_transaction = frappe.new_doc("Library Transaction")
        new_transaction.type = "Issue"
        new_transaction.books = "Test Book"
        new_transaction.library_member = "Test Member" # Test member here (different from existing transaction)
        new_transaction.issue_date = frappe.utils.today()
        new_transaction.return_date = frappe.utils.add_days(frappe.utils.today(), 5)

        # 3. Assert that submitting the new transaction does *not* raise an exception
        try:
            new_transaction.submit()
        except ValidationError:
            self.fail("ValidationError should not be raised for different member")

    def test_duplicate_book_borrowing_allowed_returned_book(self):
        # Test case: Borrowing same book is allowed after returning the previous copy

        # 1. Create and submit an existing 'Issue' transaction
        existing_transaction = frappe.get_doc({
            "doctype": "Library Transaction",
            "type": "Issue",
            "books": "Test Book",
            "library_member": "Test Member",
            "issue_date": frappe.utils.today(),
            "return_date": frappe.utils.add_days(frappe.utils.today(), 5),
        }).insert()
        existing_transaction.submit()

        # 2. Cancel the existing transaction (simulating book return)
        existing_transaction.cancel() # Assuming you have cancel functionality

        # 3. Attempt to create a new 'Issue' transaction for the same member and book
        new_transaction = frappe.new_doc("Library Transaction")
        new_transaction.type = "Issue"
        new_transaction.books = "Test Book"
        new_transaction.library_member = "Test Member"
        new_transaction.issue_date = frappe.utils.today()
        new_transaction.return_date = frappe.utils.add_days(frappe.utils.today(), 5)

        # 4. Assert that submitting the new transaction does *not* raise an exception
        try:
            new_transaction.submit()
        except ValidationError:
            self.fail("ValidationError should not be raised after book return")