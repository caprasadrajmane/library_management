// Copyright (c) 2024, Prasad Rajmane and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book Transaction", {
	refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.add_custom_button(
                __("Book Ledger"),
                () => {
                    frappe.route_options = {
                        voucher_no: frm.doc.name,
                    },
                    frappe.set_route("query-report", "Book Ledger")
                },
                __("View")
            );
        }
	},
});
