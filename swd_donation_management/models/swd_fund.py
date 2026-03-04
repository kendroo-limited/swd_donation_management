from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_donor = fields.Boolean(string="Is Donor")
    donor_code = fields.Char(string="Donor Code")


class SwdFund(models.Model):
    _name = "swd.fund"
    _description = "SWD Fund"

    name = fields.Char(required=True)
    code = fields.Char()
    donor_id = fields.Many2one(
        "res.partner",
        string="Primary Donor",
        domain=[("is_donor", "=", True)],
    )
    fund_type = fields.Selection(
        [
            ("general", "General"),
            ("project", "Project"),
            ("grant", "Grant"),
            ("donation", "Donation"),
        ],
        default="general",
        required=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id.id,
    )
    contribution_ids = fields.One2many("swd.contribution", "fund_id")
    subsidy_ids = fields.One2many("swd.subsidy", "fund_id")
    project_ids = fields.One2many("swd.project", "fund_id")
    total_contributed = fields.Monetary(
        compute="_compute_totals", store=True, currency_field="currency_id"
    )
    total_subsidized = fields.Monetary(
        compute="_compute_totals", store=True, currency_field="currency_id"
    )
    balance = fields.Monetary(
        compute="_compute_totals", store=True, currency_field="currency_id"
    )
    active = fields.Boolean(default=True)

    @api.depends("contribution_ids.amount", "subsidy_ids.amount", "subsidy_ids.state")
    def _compute_totals(self):
        for fund in self:
            fund.total_contributed = sum(fund.contribution_ids.mapped("amount"))
            approved = fund.subsidy_ids.filtered(lambda s: s.state != "cancelled")
            fund.total_subsidized = sum(approved.mapped("amount"))
            fund.balance = fund.total_contributed - fund.total_subsidized


class SwdContribution(models.Model):
    _name = "swd.contribution"
    _description = "SWD Contribution"

    fund_id = fields.Many2one("swd.fund", required=True)
    donor_id = fields.Many2one(
        "res.partner",
        domain=[("is_donor", "=", True)],
        required=True,
    )
    date = fields.Date(default=fields.Date.context_today)
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one(
        "res.currency", related="fund_id.currency_id", store=True
    )
    reference = fields.Char()
    notes = fields.Text()


class SwdProject(models.Model):
    _name = "swd.project"
    _description = "SWD Project/Grant"

    name = fields.Char(required=True)
    code = fields.Char()
    fund_id = fields.Many2one("swd.fund")
    department_id = fields.Many2one("hr.department")
    description = fields.Text()
    active = fields.Boolean(default=True)
