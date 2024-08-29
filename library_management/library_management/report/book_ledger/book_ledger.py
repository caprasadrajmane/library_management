# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = [
        {"label": "Voucher #", "fieldtype": "Data", "fieldname": "voucher_no"},
        {"label": "Date", "fieldtype": "Date", "fieldname": "date"},
        {
            "label": "Transaction Type",
            "fieldtype": "Select",
            "fieldname": "transaction_type",
            "options": ["Book Inward", "Book Outward"],
        },
        {"label": "Description", "fieldtype": "Data", "fieldname": "description"},
        {"label": "Book", "fieldtype": "Link", "fieldname": "book", "options": "Book"},
        {
            "label": "Warehouse",
            "fieldtype": "Link",
            "fieldname": "warehouse",
            "options": "Library Warehouse",
        },
        {
            "label": "Library Member",
            "fieldtype": "Link",
            "fieldname": "library_member",
            "options": "Library Member",
        },
        {"label": "Quantity", "fieldtype": "Int", "fieldname": "quantity"},
    ]

    conditions = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    voucher_no = filters.get("voucher_no")
    book = filters.get("book")

    conditions["date"] = ["between", [from_date, to_date]]
    if voucher_no:
        conditions["voucher_no"] = voucher_no
    if book:
        conditions["book"] = book

    data = frappe.db.get_all("Book Ledger Entry", fields=["*"], filters=conditions)

    return columns, data
