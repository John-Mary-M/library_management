import frappe
from frappe import _
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def login():
    # Retrieve form values
    usr = frappe.form_dict.get("usr")
    pwd = frappe.form_dict.get("pwd")
    
    try:
        # Initialize the login manager and attempt authentication
        login_manager = LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()  # Set session, etc.
        
        # Return a JSON response with a redirect URL
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/books"  # list of books
    except frappe.AuthenticationError:
        # Raise an error if authentication fails
        frappe.throw(_("Invalid username or password"), frappe.AuthenticationError)
