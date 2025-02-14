from odoo import models, fields

class User(models.Model):
    _name = "chessknight.user"
    _description = "This is the user model"

    name = fields.Char(
        string='Name',
        help='Description of the field')
    