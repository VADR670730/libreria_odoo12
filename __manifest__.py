# -*- coding: utf-8 -*-
{
    'name': "Libreria",

    'summary': """
        Modulo de libreria""",

    'description': """
        Pruebas en casa
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/ventaLibro.xml',
        'views/reporte_libreria.xml',
        'views/reporte_libreria_pdf.xml',
        'views/reporte_libreria_excel.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}