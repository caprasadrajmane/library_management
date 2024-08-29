// Copyright (c) 2024, Prasad Rajmane and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book", {
	refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(
                __("Book Ledger"),
                () => {
                    frappe.route_options = {
                        book: frm.doc.name,
                    },
                    frappe.set_route("query-report", "Book Ledger")
                },
                __("View")
            );
        }
	},
});
