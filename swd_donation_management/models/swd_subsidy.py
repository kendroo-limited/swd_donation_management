from odoo import api, fields, models


class SwdSubcenter(models.Model):
    _name = "swd.subcenter"
    _description = "SWD Subcenter"

    name = fields.Char(required=True)
    code = fields.Char()
    location = fields.Char()
    active = fields.Boolean(default=True)


class SwdSubsidy(models.Model):
    _name = "swd.subsidy"
    _description = "SWD Subsidy"

    name = fields.Char(default="New", readonly=True)
    patient_id = fields.Many2one("swd.patient", required=True)
    category_id = fields.Many2one(
        "swd.patient.category",
        string="Patient Category",
    )
    patient_type = fields.Selection(related="patient_id.patient_type", store=True)
    case_type = fields.Selection(
        [
            ("sci", "SCI"),
            ("out_patient", "Out-patient"),
            ("other", "Other"),
        ],
        default="other",
        required=True,
    )
    fund_id = fields.Many2one("swd.fund", required=True)
    project_id = fields.Many2one("swd.project")
    department_id = fields.Many2one("hr.department")
    subcenter_id = fields.Many2one("swd.subcenter")
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one(
        "res.currency", related="fund_id.currency_id", store=True
    )
    date = fields.Date(default=fields.Date.context_today)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("approved", "Approved"),
            ("paid", "Paid"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
    )
    eligibility_criteria = fields.Text()
    has_required_reports = fields.Boolean(string="Required Reports Attached")
    notes = fields.Text()

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("swd.subsidy") or "New"
        return super().create(vals)

    @api.onchange("patient_id")
    def _onchange_patient(self):
        if self.patient_id:
            self.category_id = self.patient_id.category_id

    def action_set_draft(self):
        self.write({"state": "draft"})

    def action_approve(self):
        self.write({"state": "approved"})

    def action_mark_paid(self):
        self.write({"state": "paid"})

    def action_cancel(self):
        self.write({"state": "cancelled"})
