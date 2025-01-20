from odoo import models, fields

class Profesor(models.Model):
    _name = "instituto.profesor"
    _description = "Este es el modelo del profesor"
    
    DNI = fields.Char(        
        string="Documento Nacional de Identidad",
        help="Caracteres de identificación de un usuario",
        size=9,
        index=True,
        required=True)

    stringName = fields.Char(
        string='Nombre',
        help='Nombre del profesor')
    dateBirth = fields.Date(
        string='Fecha de Nacimiento',
        help='Fecha de Nacimiento del profesor')
    active = fields.Boolean(
        'Activo',
        help="El profesor esta dando clase o no",
        readonly=True,
        default=False)
    