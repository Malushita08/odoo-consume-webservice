from odoo import models, fields


class kds_res_config_settings(models.TransientModel):
    # Inherit fields from res.config.settings
    _inherit = 'res.config.settings'

    # Add the needed field to save webservice url
    webservice_url = fields.Char(related='company_id.webservice_url', readonly=False)
    webservice_token = fields.Char(related='company_id.webservice_token', readonly=False)
