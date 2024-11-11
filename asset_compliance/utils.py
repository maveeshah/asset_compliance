import frappe
from frappe.utils import add_days, add_months, add_years, getdate, nowdate


@frappe.whitelist()
def custom_calculate_next_due_date(
    periodicity,
    start_date=None,
    end_date=None,
    last_completion_date=None,
    next_due_date=None,
):
    if not start_date and not last_completion_date:
        start_date = frappe.utils.now()

    if last_completion_date and (
        (start_date and last_completion_date > start_date) or not start_date
    ):
        start_date = last_completion_date
    if periodicity == "Daily":
        next_due_date = add_days(start_date, 1)
    if periodicity == "Weekly":
        next_due_date = add_days(start_date, 7)
    if periodicity == "Monthly":
        next_due_date = add_months(start_date, 1)
    if periodicity == "Quarterly":
        next_due_date = add_months(start_date, 3)
    if periodicity == "Half-yearly":
        next_due_date = add_months(start_date, 6)
    if periodicity == "Yearly":
        next_due_date = add_years(start_date, 1)
    if periodicity == "2 Yearly":
        next_due_date = add_years(start_date, 2)
    if periodicity == "3 Yearly":
        next_due_date = add_years(start_date, 3)
    if periodicity == "4 Yearly":
        next_due_date = add_years(start_date, 4)
    if periodicity == "5 Yearly":
        next_due_date = add_years(start_date, 5)
    if periodicity == "6 Yearly":
        next_due_date = add_years(start_date, 6)
    if end_date and (
        (start_date and start_date >= end_date)
        or (last_completion_date and last_completion_date >= end_date)
        or next_due_date
    ):
        next_due_date = ""
    return next_due_date


def add_option_to_periodicity():
    periodicity = frappe.get_meta("Asset Maintenance Task").get_field("periodicity")
    periodicity.options = "Daily\nWeekly\nMonthly\nQuarterly\nHalf-yearly\nYearly\n2 Yearly\n3 Yearly\n4 Yearly\n5 Yearly\n6 Yearly"
    periodicity.save(ignore_permissions=True)
    frappe.db.commit()
