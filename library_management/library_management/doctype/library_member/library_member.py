# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LibraryMember(Document):
    def before_validate(doc):
        doc.full_name = f"{doc.first_name} {doc.last_name}"
