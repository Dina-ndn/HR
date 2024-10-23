# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime


class HrEmployeeInformation(models.Model):
    _name = "hr.employee.information"
    _description = "Employee Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Employee Name",required=True)
    department_id = fields.Many2one('hr.department','Department')
    staff_id = fields.Char(string="Staff ID")
    job_id = fields.Many2one('hr.job','Job Position')
    # employee_image = fields.Binary(string="Employee Image",attachment="True")
    # company_id = fields.Many2one('res.company',required=True)
    # company_country_id = fields.Many2one('res.country', 'Company Country', related='company_id.country_id', readonly=True)
    # company_country_code = fields.Char(related='company_country_id.code', readonly=True)

    # Get Process
    # employee_id = fields.Many2one('hr.employee', string='Process')
    number_of_process = fields.Integer(string="NumberOfProcesses",compute="get_number_of_process")
    number_of_process_name = fields.Char(string="Processes",compute="get_number_of_process",default='-')
    show_process_name = fields.Text(string="Product", compute="get_process_name")

    # Number of Process for each employee
    def get_number_of_process(self):
        for process in self:
            process.env.cr.execute("""select count(hr_employee.id) from hr_employee
                                    where hr_employee.emp_info_ids=%s""" % (process.id))
            res = self.env.cr.fetchone()
            process.number_of_process = res and res[0] or 0.0

            # Get Process Name
            process.env.cr.execute("""select hr_employee.name from hr_employee
                                    where hr_employee.emp_info_ids=%s""" % (process.id))
            res = self.env.cr.fetchall()
            process.number_of_process_name = res or ' '
            # process.number_of_process_name.split(',')[0]: self.env.cr.fetchall()[0][0]
    # private Information

    @api.depends('number_of_process_name')
    def get_process_name(self):
        for rec in self:
            rec.show_process_name = rec.number_of_process_name.strip("[]").strip("()").strip(",").replace(",), (", ", ").replace("'", "")

    private_email = fields.Char(string="Private Email")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], tracking=True)
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', default='single', tracking=True)
    spouse_complete_name = fields.Char(string="Spouse Complete Name", tracking=True)
    spouse_birthdate = fields.Date(string="Spouse Birthdate", tracking=True)
    children = fields.Integer(string='Number of Children', tracking=True)
    place_of_birth = fields.Char('Place of Birth', tracking=True)
    country_of_birth = fields.Many2one('res.country', string="Country of Birth", tracking=True)
    birthday = fields.Date('Date of Birth', tracking=True)
    ssnid = fields.Char('SSN No', help='Social Security Number', tracking=True)
    sinid = fields.Char('SIN No', help='Social Insurance Number', tracking=True)
    identification_id = fields.Char(string='Identification No', tracking=True)
    passport_id = fields.Char('Passport No', tracking=True)
    permit_no = fields.Char('Work Permit No', tracking=True)
    visa_no = fields.Char('Visa No', tracking=True)
    visa_expire = fields.Date('Visa Expire Date', tracking=True)
    work_permit_expiration_date = fields.Date('Work Permit Expiration Date', tracking=True)
    has_work_permit = fields.Binary(string="Work Permit", tracking=True)
    work_permit_scheduled_activity = fields.Boolean(default=False)
    additional_note = fields.Text(string='Additional Note', tracking=True)
    certificate = fields.Selection([
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ], 'Certificate Level', default='other', tracking=True)
    study_field = fields.Char("Field of Study", tracking=True)
    study_school = fields.Char("School", tracking=True)
    emergency_contact = fields.Char("Emergency Contact", tracking=True)
    emergency_phone = fields.Char("Emergency Phone", tracking=True)
    km_home_work = fields.Integer(string="Home-Work Distance", tracking=True)
    phone = fields.Integer(string="Private Phone")

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            result.append((rec.id,name))
        return result
    
    # @api.depends('employee_id')
    # def _get_employee_data(self):
    #     for rec in self:
    #         rec.department_id = rec.employee_id.department_id
    #         rec.job_id = rec.employee_id.job_id
            