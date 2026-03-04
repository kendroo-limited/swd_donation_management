from odoo import fields, models


class SwdPatientCategory(models.Model):
    _name = "swd.patient.category"
    _description = "SWD Patient Category"

    name = fields.Char(required=True)
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)


class SwdPatient(models.Model):
    _name = "swd.patient"
    _description = "SWD Patient"

    name = fields.Many2one("hms.patient", required=True)
    partner_id = fields.Many2one("res.partner")
    category_id = fields.Many2one("swd.patient.category", string="Category")
    patient_type = fields.Selection(
        [
            ("sci", "SCI Patient"),
            ("out_patient", "Out-patient"),
            ("staff", "Staff"),
            ("staff_dependent", "Dependent of Staff"),
            ("student", "CRP Student"),
            ("trainee", "CRP MMVII Trainee"),
            ("other", "Other"),
        ],
        default="other",
        required=True,
    )
    socioeconomic_status = fields.Selection(
        [
            ("low", "Low"),
            ("middle", "Middle"),
            ("high", "High"),
            ("unknown", "Unknown"),
        ],
        default="unknown",
        required=True,
    )
    eligibility_notes = fields.Text(string="Eligibility Notes")
    active = fields.Boolean(default=True)
