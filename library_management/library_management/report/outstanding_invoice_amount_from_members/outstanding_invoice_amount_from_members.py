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
			"label": "Total Due",
			"fieldname": "outstanding",
			"fieldtype": "Float"
		},
	]

	query = f"""
		SELECT `library_member`, sum(`total_amount`) as outstanding
		FROM `tabBook Rent Invoice` 
		WHERE `status`='Unpaid'
		GROUP BY `library_member`
		HAVING outstanding > 0
	"""
	data = frappe.db.sql(query, as_dict=True)
	
	return columns, data
