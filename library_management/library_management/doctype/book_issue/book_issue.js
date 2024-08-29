// Copyright (c) 2024, Prasad Rajmane and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book Issue", {
  refresh: (frm) => {
    if (frm.doc.docstatus === 1 && frm.doc.status === "Issued") {
      frm.add_custom_button(
        __("Book Receipt"),
        () => {
          frappe.model.open_mapped_doc({
            method:
              "library_management.library_management.doctype.book_issue.book_issue.make_book_receipt",
            frm: frm,
          });
        },
        __("Create")
      );
    }
    if (frm.doc.docstatus === 1) {
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

  date: async (frm) => {
    let max_days = await frappe.db.get_single_value(
      "Library Settings",
      "maximum_book_lending_days"
    );
    let expected_return_date = frappe.datetime.add_days(frm.doc.date, max_days);
    frm.set_value("expected_return_date", expected_return_date);
    frm.refresh_field("expected_return_date");
  },
});
