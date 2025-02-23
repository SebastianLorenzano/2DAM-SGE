# __manifest__.py
# -*- coding: utf-8 -*-

{
    'name': 'ChessKnight',
    'version': '0.0.0',
    'author': "Sebastian Lorenzano",
    'maintainer': "Sebastian Lorenzano",
    'category': 'Juegos/ChessKnight',
    'sequence': 1,
    'summary': 'Aplicación de ChessKnight de Odoo',
    'description': """
        Aplicación de ChessKnight de Odoo"
    """,
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/chessknight_groups.xml',
        'views/menu.xml',
             ],
    'demo': [],

    'application': True,
    
} 