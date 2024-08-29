// Copyright (c) 2024, Prasad Rajmane and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book Rent Invoice", {
  refresh(frm) {
    if (frm.doc.docstatus === 1 && frm.doc.status === "Unpaid") {
      frm.add_custom_button(
        __("Payment Advice"),
        () => {
          frappe.model.open_mapped_doc({
            method:
              "library_management.library_management.doctype.book_rent_invoice.book_rent_invoice.make_payment_voucher",
            frm: frm,
          });
        },
        __("Create")
      );
    }
  },
});

frappe.ui.form.on("Book Rent Invoice Item", {
  refresh: (frm) => {},

  issue_date: (frm, cdt, cdn) => {
    frm.trigger("update_days", cdt, cdn);
  },

  return_date: (frm, cdt, cdn) => {
    frm.trigger("update_days", cdt, cdn);
  },

  update_days: async (frm, cdt, cdn) => {
    let item = locals[cdt][cdn];

    if (item.issue_date && item.return_date) {
      let rent_per_day = await frappe.db.get_single_value(
        "Library Settings",
        "book_lending_charges_per_day"
      );

      let days = frappe.datetime.get_day_diff(
        item.return_date,
        item.issue_date
      );

      frappe.model.set_value(cdt, cdn, "days", days);
      frappe.model.set_value(cdt, cdn, "rent_per_day", rent_per_day);
      frappe.model.set_value(cdt, cdn, "amount", days * rent_per_day);

      frm.refresh_field("items");
    }
  },
});
