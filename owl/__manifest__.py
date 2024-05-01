# -*- coding: utf-8 -*-
{
    'name' : 'OWL Tutorial',
    'version' : '1.0',
    'summary': 'OWL Tutorial',
    'sequence': -1,
    'description': """OWL Tutorial""",
    'category': 'OWL',
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl/static/src/components/*/*.js',
            'owl/static/src/components/*/*.scss',
            'owl/static/src/components/*/*.xml',
        ],
        # FOR ODOO PRE 17
        # 'web.assets_qweb': [
        #     'owl/static/src/components/*/*.xml',
        # ],
    },
}