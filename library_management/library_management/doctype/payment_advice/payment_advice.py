# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PaymentAdvice(Document):
    def on_submit(doc):
        frappe.db.set_value(
            "Book Rent Invoice", doc.book_rent_invoice_reference, {"status": "Paid"}
        )
        frappe.db.commit()
