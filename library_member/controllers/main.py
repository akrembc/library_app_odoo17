from odoo import http

from odoo.addons.library_app.controllers.main import Books


class BooksExtended(Books):

    @http.route()
    def book_list(self, **kwargs):
        response = super().book_list(**kwargs)
        if kwargs.get("available"): # if it just existed (no matter what value)
            all_books = response.qcontext["books"]
            available_books = all_books.filtered("is_available")
            response.qcontext["books"] = available_books
        return response
