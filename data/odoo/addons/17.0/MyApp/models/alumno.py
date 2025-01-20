from odoo import models, fields

class Alumno(models.Model):
    _name = "instituto.alumno"
    _description = "Este es el modelo del alumno"
    
    DNI = fields.Char(        
        string="Documento Nacional de Identidad",
        help="Caracteres de identificación de un usuario",
        size=9,
        index=True,
        required=True)

    stringName = fields.Char(
        string='Nombre',
        help='Descripción del campo')
    dateBirth = fields.Date(
        string='Fecha de Nacimiento',
        help='Descripción del campo')
    passed = fields.Boolean(
        'Aprovado',
        help="El alumno ha aprovado o no",
        readonly=True,
        default=False)
    



