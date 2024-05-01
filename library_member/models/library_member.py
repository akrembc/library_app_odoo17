from odoo import fields, models, api

class Member(models.Model):

    _name = "library.member"

    _description = "Library Member"

    card_number = fields.Char(string="Card Number")

    _inherit = ["mail.thread", "mail.activity.mixin"]

    # name = fields.Char(
    #     change_default="False",
    #     company_dependent="False",
    #     string="Member Name",
    #     trim="True",
    #     default="My Name"
    # ),

    partner_id = fields.Many2one(
        "res.partner",
        delegate=True,  # as an alternative to _inherits = {"res.partner": "partner_id"}
        ondelete="cascade",
        required=True,
    )
    
    
    def open_modal(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Message',
            'view_mode': 'form',
            'res_model': 'library.modal',
            'target': 'new',
            'context': {
                'message': 'Hello World!',
            },
        }

