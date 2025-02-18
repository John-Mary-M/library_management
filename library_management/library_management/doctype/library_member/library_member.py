# Copyright (c) 2025, LuxTech and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class LibraryMember(WebsiteGenerator):

    def before_save(self):
        """fills in the fullname readonly field we setup in the doctype"""
        self.full_name = f'{self.first_name} {self.last_name or ""}'
