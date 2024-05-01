from odoo import models, fields

class MyModal(models.TransientModel):
    _name = 'library.modal'
    _description = 'My Modal'
    _transient = True

    message  = fields.Char("My Message")
    # Fields definition here