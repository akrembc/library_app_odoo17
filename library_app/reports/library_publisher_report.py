from odoo import api, models


class PublisherReport(models.AbstractModel):

    _name = "report.library_app.publisher_report"
    _description = "Book Publisher Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        books = self.env["library.book"].search([("publisher_id", "in", docids)])

        publishers = books.mapped("publisher_id")
        publisher_books = [
            (pub, books.filtered(lambda book: book.publisher_id == pub))
            for pub in publishers
        ]
        docargs = {
            "publisher_books": publisher_books,
        }

        return docargs