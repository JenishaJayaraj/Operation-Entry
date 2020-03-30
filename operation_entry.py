from __future__ import unicode_literals
import frappe
import datetime
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe.utils import (flt, cint, time_diff_in_hours, get_datetime, getdate,
	get_time, add_to_date, time_diff, add_days, get_datetime_str,now_datetime)
from erpnext.manufacturing.doctype.manufacturing_settings.manufacturing_settings import get_mins_between_operations


@frappe.whitelist()
for d in self.operation_details:
    if d.work_order:
        job_card = frappe.new_doc("Job Card")
        job_card.work_order = d.work_order
        job_card.workstation = self.workstation
        job_card.operation = self.operation
        job_card.docstatus = 0
        job_card.append({
            "from_time": d.start_time,
            "to_time": d.end_time,
            "completed_qty": d.completed_qty
        })
        job_card.save(ignore_permissions=True)
        frappe.msgprint("Job card Created")
