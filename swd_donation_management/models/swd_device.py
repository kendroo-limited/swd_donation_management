from odoo import fields, models


class SwdDevice(models.Model):
    _name = "swd.device"
    _description = "SWD Assistive Device"

    name = fields.Char(required=True)
    device_number = fields.Char()
    device_type = fields.Selection(
        [
            ("wheelchair", "Wheelchair"),
            ("prosthetic", "Prosthetic"),
            ("aid", "Aid"),
            ("other", "Other"),
        ],
        default="other",
        required=True,
    )
    patient_id = fields.Many2one("swd.patient")
    issue_date = fields.Date(default=fields.Date.context_today)
    return_date = fields.Date()
    state = fields.Selection(
        [
            ("available", "Available"),
            ("issued", "Issued"),
            ("returned", "Returned"),
            ("lost", "Lost"),
        ],
        default="available",
        required=True,
    )
    notes = fields.Text()

    def action_mark_issued(self):
        self.write({"state": "issued"})

    def action_mark_returned(self):
        self.write({"state": "returned"})

    def action_mark_lost(self):
        self.write({"state": "lost"})

    def action_mark_available(self):
        self.write({"state": "available"})
