# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
		{
			"label": "Library Member",
			"fieldname": "library_member",
			"fieldtype": "Link",
			"options": "Library Member"
		},
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

	query = f"""
		SELECT `book`, `library_member`, sum(`quantity`) as stock_quantity 
		FROM `tabBook Ledger Entry` 
		WHERE `warehouse`='Out Library' 
		GROUP BY `book`
		HAVING stock_quantity > 0
	"""
	data = frappe.db.sql(query, as_dict=True)
	return columns, data
