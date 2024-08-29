# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import nowdate


class BookRentInvoice(Document):
    def on_submit(doc):
        frappe.db.set_value(
            "Book Return", doc.book_return_reference, {"status": "Invoiced"}
        )
        frappe.db.commit()


@frappe.whitelist()
def make_payment_voucher(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.date = nowdate()
        target.mode_of_payment = "Cash"

    doclist = get_mapped_doc(
        "Book Rent Invoice",
        source_name,
        {
            "Book Rent Invoice": {
                "doctype": "Payment Advice",
                "field_map": {
                    "name": "book_rent_invoice_reference",
                    "total_amount": "amount",
                    "library_member": "library_member",
                },
            }
        },
        target_doc,
        set_missing_values,
    )

    return doclist
