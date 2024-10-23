# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import babel
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from pytz import timezone
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class HrEmployeeOt(models.Model):
    _name = "hr.employee.ot"
    _description = "Employee Overtime"
    _rec_name = 'employee_id'
    # _order = 'delivery_date desc'

    def _default_employee(self):
        return self.env.user.employee_id

    employee_id = fields.Many2one(
        'hr.employee', string="Employee", default=_default_employee,
        required=True, ondelete='cascade', index=True)
    time_from = fields.Datetime(string="Time From", default=fields.Datetime.now, required=True)
    time_to = fields.Datetime(string="Time To")
    overtime_hours = fields.Float(string='Number of Overtime (Hr)', compute='_compute_overtime_hours', index=True, copy=False, store=True, readonly=False)
    
    @api.depends('time_from', 'time_to')
    def _compute_overtime_hours(self):
        for overtime in self:
            if overtime.time_to and overtime.time_from:
                delta = overtime.time_to - overtime.time_from
                overtime.overtime_hours = delta.total_seconds() / 3600.0
            else:
                overtime.overtime_hours = False
    
    @api.constrains('time_from', 'time_to')
    def _check_dates(self):
        if any(self.filtered(lambda overtime: overtime.time_from > overtime.time_to)):
            raise ValidationError(_("Overtime 'Time From' must be earlier 'Time To'."))
            

            
