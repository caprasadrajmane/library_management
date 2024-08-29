import frappe
from frappe.utils import nowdate, getdate


def get_accrued_income():
    query = f"""
		SELECT i.date, count(b.book) as book_count, i.name as book_issue, i.library_member
		FROM `tabBook Issue Item` as b
		LEFT JOIN `tabBook Issue` as i
		ON b.parent = i.name
		WHERE i.status='Issued'
		AND i.docstatus = 1
		GROUP BY i.date, i.name
	"""
    data = frappe.db.sql(query, as_dict=True)
    rent_per_day = frappe.db.get_single_value("Library Settings", "book_lending_charges_per_day")
    current_date = getdate(nowdate())
    for item in data:
        transaction_date = getdate(item["date"])
        days_difference = (current_date - transaction_date).days
        item["current_date"] = current_date
        item["rent_per_day"] = rent_per_day
        item["days_difference"] = days_difference
        item["total_outstanding"] = rent_per_day * days_difference * item["book_count"]

    return data
