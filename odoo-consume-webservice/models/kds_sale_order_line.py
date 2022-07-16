from odoo import models, fields
import requests


class kds_sale_order_line(models.Model):
    # Inherit fields from sale order
    _inherit = ['sale.order.line']

    # # Add the needed fields to save webservice data
    kds_id_precio = fields.Char(string='kds_id_precio')
    kds_id_precio1 = fields.Char(string='kds_id_precio1')
