from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Book(models.Model):

    _name = "library.book"
    _description = "Book"
    _order = "name, date_published desc"

    # the following 4 attributes will no effect
    _rec_name = "name"
    _table = "library_book"
    _log_access = True
    _auto = True

    # String fields:
    name = fields.Char("Title", required=True)
    isbn = fields.Char("ISBN")
    book_type = fields.Selection([("paper", "Paperback"),
                                  ("hard", "Hardcover"),
                                  ("electronic", "Electronic"),
                                  ("other", "Other")], "Type")
    notes = fields.Text("Internal Notes")
    descr = fields.Html("Description")

    # Numeric fields:
    copies = fields.Integer(default=1)
    avg_rating = fields.Float("Average Rating", (3, 2))
    price = fields.Monetary("Price", "currency_id")

    # price helper
    currency_id = fields.Many2one("res.currency")

    # Date and time fields:
    date_published = fields.Date()
    last_borrow_date = fields.Datetime(
        "Last Borrowed On",
        default=lambda self: fields.Datetime.now(),
    )

    # Other fields:
    active = fields.Boolean("Active?", default=True)
    image = fields.Binary("Cover")
    publisher_id = fields.Many2one("res.partner", string="Publisher")
    author_ids = fields.Many2many("res.partner", string="Authors")

    publisher_country_id = fields.Many2one(
        "res.country",
        string="Publisher Country",
        related="publisher_id.country_id",
        readonly=False
    )

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:  # it also add a WARNING in the terminal
                raise ValidationError("Please provide an ISBN for %s" %
                                      book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is invalid" % book.isbn)
            # if book._check_isbn(): # should add validation styling on ISBN input
            #     raise ValidationError("%s ISBN is valid" % book.isbn)
        return True
    
    _sql_constraints = [
        ("library_book_name_date_uq",
        "UNIQUE (name, date_published)",
        "Title and publication date must be unique."),
        ("library_book_check_date",
        "CHECK (date_published <= current_date)",
        "Publication date must not be in the future."),
    ]

    @api.constrains("isbn")
    def _constrain_isbn_valid(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s is an invalid ISBN" % book.isbn)