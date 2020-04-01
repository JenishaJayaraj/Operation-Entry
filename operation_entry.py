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
def create_job_cards(self,method):
	for d in self.operation_details:
		job_card_list = frappe.get_value("Job Card",{"work_order":d.work_order,"docstatus":1},["work_order"])
		if d.work_order != job_card_list:
			job_card = frappe.new_doc("Job Card")
			job_card.work_order = d.work_order
			job_card.workstation = self.workstation
			job_card.operation = self.operation
			job_card.for_quantity = d.for_quantity
			job_card.wip_warehouse = d.wip_warehouse
			job_card.docstatus = 1
			job_card.employee = self.operator_name
			job_card.append("time_logs",{
			    "from_time": d.start_time,
			    "to_time": d.end_time,
			    "completed_qty": d.completed_qty
			})
			job_card.save(ignore_permissions=True)
			frappe.msgprint(_("Job Card {0} Created").format(job_card.name))


@frappe.whitelist()
def on_cancel_op(self,method):
    for d in self.operation_details:
        job_card_list = frappe.get_list("Job Card",filters={"work_order":d.work_order,"docstatus":1},fields=["name"])
        if self.docstatus == 2:
            for j in job_card_list:
                doc = frappe.get_doc("Job Card",j.name)
                doc.docstatus = 2
                doc.save(ignore_permissions=True)
                frappe.msgprint("Job card cancelled")



@frappe.whitelist()
def update_wo_op(self,method):
    doc = frappe.get_doc("Work Order",self.work_order)
    for j in self.time_logs:
    	if j.completed_qty:
    		for d in doc.operations:
    			d.completed_qty = j.completed_qty
    			d.status = "Completed"
    			d.time_in_mins = j.time_in_mins
    			d.actual_operation_time = self.total_time_in_mins
    			d.planned_start_time = j.from_time
    			d.planned_end_time = j.to_time
    			d.actual_start_time = j.from_time
    			d.actual_end_time = j.to_time
    			doc.save(ignore_permissions=True)


@frappe.whitelist()
def validate_jb(self,method):
    for d in self.operation_details:
        job_card_list = frappe.get_list("Job Card",filters={"work_order":d.work_order,"docstatus":1},fields=["work_order"])
        for j in job_card_list:
            if d.work_order == j.work_order:
                frappe.msgprint(_("Job Card with work order {0} already Exist").format(d.work_order))



@frappe.whitelist()
def update_wo_ops(self,method):
	doc = frappe.get_doc("Work Order",self.work_order)
	for j in self.time_logs:
		if(self.docstatus) == 2:
			for d in doc.operations:
				if self.operation == d.operation:
					d.completed_qty = 0
					d.status = "Pending"
					doc.save(ignore_permissions=True)
