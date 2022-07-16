from odoo import models, fields
import requests


class kds_product_product(models.Model):
    # Inherit fields from sale order
    _inherit = ['product.product']

    # # Add the needed fields to save webservice data
    kds_id_producto = fields.Char(string='kds_id_producto')
