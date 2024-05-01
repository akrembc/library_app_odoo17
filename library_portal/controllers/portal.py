from odoo.http import route, request

from odoo.addons.portal.controllers import portal


class CustomerPortal(portal.CustomerPortal):

    def __init__(self):
        self._items_per_page = 2

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if "book_checkout_count" in counters:
            count = request.env["library.checkout"].search_count([])
            values["book_checkout_count"] = count

        return values


    @route(["/my/book-checkouts", "/my/book-checkouts/page/<int:page>"], auth="user", website=True)
    def my_book_checkouts(self, page=1, **kw):
        Checkout = request.env["library.checkout"]
        domain = []

        # Prepare pager data
        checkout_count = Checkout.search_count(domain)
        pager_data = portal.pager(
            url="/my/book-checkouts",
            total=checkout_count,
            page=page,
            step=self._items_per_page,
        )
        print(f"\n\n{pager_data}\n\n")
        # Recordset according to pager and domain filter
        checkouts = Checkout.search(
            domain,
            limit=self._items_per_page,
            offset=pager_data["offset"],
        )
        # Prepare template values and render
        values = self._prepare_portal_layout_values()
        values.update(
            {
                "checkouts": checkouts,
                "page_name": "book-checkouts",
                "default_url": "/my/book-checkouts",
                "pager": pager_data,
            }
        )
        return request.render(
            "library_portal.my_book_checkouts",
            values
        )


    @route(["/my/book-checkout/<model('library.checkout'):doc>"], auth="user", website=True)
    def my_checkout_details(self, doc=None, **kw):
        print(f'\n\n\nI am triggered {doc}\n\n\n')
        return request.render(
            "library_portal.book_checkout",
            {"doc": doc},
        )
    

