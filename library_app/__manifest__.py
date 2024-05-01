# pylint: disable=locally-disabled, pointless-statement, missing-module-docstring
# -*- coding: utf-8 -*-
{
    "name": "Library Management",
    "summary": """
        Manage library catalog and book lending.
    """,
    "description": """
        Title

        =====

        Subtitle

        --------

        This is *emphasis*, rendered in italics.

        This is **strong emphasis**, rendered in bold.

        This is a bullet list:

        - Item one.

        - Item two.
    """,
    "author": "Akrem",
    "license": "AGPL-3",
    "website": "https://github.com/PacktPublishing" "/Odoo-15-Development-Essentials",
    "category": "Services/Library",
    "version": "17.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "mail"],
    # always loaded
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        "views/book_view.xml",
        "views/library_menu.xml",
        "views/book_list_template.xml",
        "reports/library_book_report.xml",
        "reports/library_publisher_report.xml",
    ],
    # only loaded in demonstration mode
    # "demo": [
    #     "data/my_partner.xml",
    # ],
    "application": True,
    "sequence": -1,
}
