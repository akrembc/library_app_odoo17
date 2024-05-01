from odoo import http
import logging

_logger = logging.getLogger(__name__)


class Books(http.Controller):

    @http.route("/library/books")
    def book_list(self, **kwargs):

        Book = http.request.env["library.book"]

        # Book.create({
        #     "name": "Odoo Development Essentials",
        #     "isbn": "879-1-78439-279-6"})

        # create(), search(), write(), and unlink() are the CRUD operations for odoo's ORM
        books = Book.search([])
        _logger.info("%s hey heeeeeeeeeeeeeeeeey" % list(books))  # .warn()

        return http.request.render("library_app.book_list_template",
                                   {"books": books})
