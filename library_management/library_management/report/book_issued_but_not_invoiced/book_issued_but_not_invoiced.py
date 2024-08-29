# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

from library_management.library_management.controllers.accrued_rent_income import (
    get_accrued_income,
)


def execute(filters=None):
    columns = [
        {
            "label": "Book Issue",
            "fieldname": "book_issue",
            "fieldtype": "Link",
            "options": "Book Issue",
        },
        {
            "label": "Library Member",
            "fieldname": "library_member",
            "fieldtype": "Link",
            "options": "Library Member",
        },
        {"label": "Current Date", "fieldname": "current_date", "fieldtype": "Date"},
        {"label": "Issue Date", "fieldname": "date", "fieldtype": "Date"},
        {"label": "No of days", "fieldname": "days_difference", "fieldtype": "Int"},
        {"label": "No of books", "fieldname": "book_count", "fieldtype": "Int"},
        {"label": "Rent per day", "fieldname": "rent_per_day", "fieldtype": "Float"},
        {
            "label": "Total Outstanding",
            "fieldname": "total_outstanding",
            "fieldtype": "Float",
        },
    ]
    data = get_accrued_income()
    return columns, data
