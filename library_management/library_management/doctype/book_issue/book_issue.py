# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import add_days, nowdate
from library_management.library_management.controllers.accrued_rent_income import (
    get_accrued_income,
)


class BookIssue(Document):
    def validate(doc):
        maximum_book_lending_days = frappe.db.get_single_value(
            "Library Settings", "maximum_book_lending_days"
        )
        max_return_date = add_days(doc.date, maximum_book_lending_days)
        if doc.expected_return_date > max_return_date:
            frappe.throw(
                f"Expected return date can not be greater than {max_return_date}"
            )

        maximum_books_issue = frappe.db.get_single_value(
            "Library Settings", "maximum_books_issue"
        )
        if len(doc.book_details) > maximum_books_issue:
            frappe.throw(
                f"Maximum {maximum_books_issue} books can be issued per transaction"
            )

    def on_submit(doc):
        for item in doc.book_details:
            book = item.book
            query = f"Select sum(quantity) as stock_quantity from `tabBook Ledger Entry` where `book`='{book}'"
            result = frappe.db.sql(query)
            sum_quantity = result[0][0] if result and result[0][0] is not None else 0
            if sum_quantity <= 0:
                frappe.throw("Book not available. Please check stock")

            ble_in = frappe.new_doc("Book Ledger Entry")
            ble_in.voucher_no = doc.name
            ble_in.date = doc.date
            ble_in.transaction_type = "Book Issue"
            ble_in.description = "Book issued"
            ble_in.book = item.book
            ble_in.warehouse = "In Library"
            ble_in.library_member = doc.library_member
            ble_in.quantity = -1
            ble_in.insert()

            ble_out = frappe.new_doc("Book Ledger Entry")
            ble_out.voucher_no = doc.name
            ble_out.date = doc.date
            ble_out.transaction_type = "Book Issue"
            ble_out.description = "Book issued"
            ble_out.book = item.book
            ble_out.warehouse = "Out Library"
            ble_out.library_member = doc.library_member
            ble_out.quantity = 1
            ble_out.insert()


@frappe.whitelist()
def make_book_receipt(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.return_date = nowdate()
        target.status = "Invoice pending"

    doclist = get_mapped_doc(
        "Book Issue",
        source_name,
        {
            "Book Issue": {
                "doctype": "Book Return",
                "field_map": {
                    "name": "book_issue_reference",
                    "library_member": "library_member",
                },
            },
            "Book Issue Item": {
                "doctype": "Book Return Item",
                "field_map": {"book": "book"},
            },
        },
        target_doc,
        set_missing_values,
    )

    return doclist


def warn_accrued_income_exceed_limit():
    data = get_accrued_income()
    defaulters = []
    max_outstanding = frappe.db.get_single_value(
        "Library Settings", "maximum_outstanding_dues__member"
    )
    for item in data:
        if item.total_outstanding > max_outstanding:
            defaulters.append(
                {
                    "Library Member": item["library_member"],
                    "Outstanding Amount": item["total_outstanding"],
                }
            )

    if len(defaulters) > 0:
        message_body = json.dumps(defaulters, indent=4)
        notification = frappe.get_doc(
            {
                "doctype": "Notification Log",
                "for_user": "caprasadrajmane@gmail.com",
                "subject": "List of Defaulters",
                "email_content": f"<pre>{message_body}</pre>",
                "type": "Alert",
            }
        )
        notification.insert(ignore_permissions=True)
        frappe.db.commit()

    print(notification)
