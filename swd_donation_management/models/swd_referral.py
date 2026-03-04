from odoo import fields, models


class SwdReferral(models.Model):
    _name = "swd.referral"
    _description = "SWD Referral"

    patient_id = fields.Many2one("swd.patient", required=True)
    msw_user_id = fields.Many2one("res.users", string="MSW Officer")
    referral_date = fields.Date(default=fields.Date.context_today)
    report_summary = fields.Text(string="Referral Report")
    active = fields.Boolean(default=True)
