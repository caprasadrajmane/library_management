// Copyright (c) 2024, Prasad Rajmane and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book Return", {
  refresh(frm) {
    if (frm.doc.docstatus === 1) {
      if (frm.doc.status === "Invoice pending") {
        frm.add_custom_button(
          __("Invoice"),
          () => {
            frappe.model.open_mapped_doc({
              method:
                "library_management.library_management.doctype.book_return.book_return.make_rent_invoice",
              frm: frm,
            });
          },
          __("Create")
        );
      }
      frm.add_custom_button(
        __("Book Ledger"),
        () => {
          (frappe.route_options = {
            voucher_no: frm.doc.name,
          }),
            frappe.set_route("query-report", "Book Ledger");
        },
        __("View")
      );
    }
  },
});
