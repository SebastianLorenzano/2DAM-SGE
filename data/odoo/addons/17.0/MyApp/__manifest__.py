# __manifest__.py
# -*- coding: utf-8 -*-

{
    'name': 'Instituto',
    'version': '0.0.0',
    'author': "Luis J. Salmerón",
    'maintainer': "Luis J. Salmerón",
    'category': 'Educación/Instituto',
    'sequence': 1,
    'summary': 'Aplicación de ejemplo para Odoo',
    'description': """
        Aplicación de ejemplo para odoo basada en unos modelos para gestionar un instituto"
    """,
    'depends': [
        'base'
    ],
    'data': ['security/instituto_groups.xml'],
    'demo': [],

    'application': True,
    
} 