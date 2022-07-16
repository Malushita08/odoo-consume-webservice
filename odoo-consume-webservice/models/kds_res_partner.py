from odoo import models, fields
import requests


class kds_res_partner(models.Model):
    # Inherit fields from sale order
    _inherit = ['res.partner']

    # Add the needed fields to save webservice data
    kds_id_cliente = fields.Char(string='kds_id_cliente')
    kds_estadodoc = fields.Char(string='kds_estadodoc')
    kds_cliente_nuevo = fields.Char(string='kds_cliente_nuevo')
    kds_estado_cliente = fields.Char(string='kds_estado_cliente')