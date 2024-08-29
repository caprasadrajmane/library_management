# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import nowdate, date_diff


class BookReturn(Document):
    def validate(doc):
        book_issue_status = frappe.db.get_value(
            "Book Issue", doc.book_issue_reference, "status"
        )
        if book_issue_status != "Issued":
            frappe.throw("Book is already returned")

    def on_submit(doc):
        frappe.db.set_value(
            "Book Issue", doc.book_issue_reference, "status", "Returned"
        )
        frappe.db.commit()

        for item in doc.book_details:
            ble_in = frappe.new_doc("Book Ledger Entry")
            ble_in.voucher_no = doc.name
            ble_in.date = doc.return_date
            ble_in.transaction_type = "Book Return"
            ble_in.description = "Book returned"
            ble_in.book = item.book
            ble_in.warehouse = "In Library"
            ble_in.library_member = doc.library_member
            ble_in.quantity = 1
            ble_in.insert()

            ble_out = frappe.new_doc("Book Ledger Entry")
            ble_out.voucher_no = doc.name
            ble_out.date = doc.return_date
            ble_out.transaction_type = "Book Return"
            ble_out.description = "Book returned"
            ble_out.book = item.book
            ble_out.warehouse = "Out Library"
            ble_out.library_member = doc.library_member
            ble_out.quantity = -1
            ble_out.insert()

    def on_cancel(doc):
        frappe.db.set_value("Book Issue", doc.book_issue_reference, "status", "Issued")
        frappe.db.commit()


@frappe.whitelist()
def make_rent_invoice(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.invoice_date = nowdate()
        target.status = "Unpaid"
        issue_date = frappe.db.get_value(
            "Book Issue", source.book_issue_reference, "date"
        )
        return_date = source.return_date
        days = date_diff(return_date, issue_date)
        rent_per_day = frappe.db.get_single_value(
            "Library Settings", "book_lending_charges_per_day"
        )
        total_amount = 0
        for item in target.items:
            total = days * rent_per_day
            item.issue_date = issue_date
            item.return_date = return_date
            item.days = days
            item.rent_per_day = rent_per_day
            item.amount = total
            total_amount += total
        target.total_amount = total_amount

    doclist = get_mapped_doc(
        "Book Return",
        source_name,
        {
            "Book Return": {
                "doctype": "Book Rent Invoice",
                "field_map": {
                    "name": "book_return_reference",
                    "library_member": "library_member",
                },
            },
            "Book Return Item": {
                "doctype": "Book Rent Invoice Item",
                "field_map": {"book": "book"},
            },
        },
        target_doc,
        set_missing_values,
    )

    return doclist
