from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)

class Book(models.Model):

    _inherit = "library.book"

    is_available = fields.Boolean("Is Available?")

    isbn = fields.Char(help="Use a valid ISBN-13 or ISBN-10.")

    publisher_id = fields.Many2one(index=True)

    def _check_isbn(self):
        self.ensure_one()
        print("Hello, world!", self.is_available)
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 10:
            ponderators = [1, 2, 3, 4, 5, 6, 7, 8, 9] # or range(1, 10)
            total = sum(a * b for a, b in zip(digits[:9], ponderators)) # [:9] useless
            check = total % 11
            return digits[-1] == check
        else:
            return super()._check_isbn()