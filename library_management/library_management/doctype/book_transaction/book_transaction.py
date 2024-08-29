# Copyright (c) 2024, Prasad Rajmane and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookTransaction(Document):

	def on_submit(self):
		for item in self.books:
			ble = frappe.new_doc("Book Ledger Entry")
			ble.voucher_no = self.name
			ble.date = self.date
			ble.transaction_type = self.transaction_type
			ble.description = self.description
			ble.book = item.book
			ble.warehouse = item.warehouse
			if self.transaction_type == "Book Inward":
				ble.quantity = item.quantity
			else:
				ble.quantity = item.quantity * -1
			ble.insert()
