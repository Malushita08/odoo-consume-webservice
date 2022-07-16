from odoo import models, fields


class kds_res_company(models.Model):
    # Inherit fields from res.company
    _inherit = 'res.company'

    # Add the needed field to save webservice url
    webservice_url = fields.Char(string="URL del webservice")
    webservice_token = fields.Char(string="Token del webservice")
