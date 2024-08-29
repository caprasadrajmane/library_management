# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
		{
			"label": "Book",
			"fieldname": "book",
			"fieldtype": "Link",
			"options": "Book"
		},
		{
			"label": "Stock",
			"fieldname": "stock_quantity",
			"fieldtype": "Float"
		},
	]
	data = frappe.db.sql(f"Select `book`, sum(`quantity`) as stock_quantity from `tabBook Ledger Entry` where `warehouse`='In Library' group by `book`", as_dict=True)
	return columns, data
