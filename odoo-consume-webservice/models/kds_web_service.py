from odoo import models, fields
import requests


class stork(models.Model):
    # Heredamos campos del modelo vehicle
    _inherit = ['sale.order']

    # FUNCIONES

    def call_web_service(self):
        # Consuminos el web service
        api_url = "http://190.85.232.41/svc/wctdm.svc/getData/"
        body = {
            "Data": {
                "consulta": "reporteventa",
                "token": "ODhmNDk5ZTQzN2YyOTAyZGE5NTc3ZTgyMzY3NDRhM2I=",
                "accion": "R",
                "Valores": [
                    "2022-06-14",
                    "2022-06-15"
                ],
                "Parametros": [
                    "@fecha_desde",
                    "@fecha_hasta"
                ]
            }
        }
        response = requests.post(api_url, json=body)

        # Recorremos el json de respuesta
        for object in response.json():
            # Creamos los objetos en las tablas

            # Cliente
            client = self.env['res.partner'].search([('name', '=', object['id_cliente'])])
            if not client:
                client = self.env['res.partner'].create({'name': object['id_cliente']})
            # Producto
            product = self.env['product.template'].search([('name', '=', object['id_producto'])])
            if not product:
                product = self.env['product.template'].create({'name': object['id_producto']})

            self.create({
                'partner_id': client.id,
                # 'order_line': [(0, 0, {'product_id': 1, 'product_uom_qty': 1, 'price_unit': 100}),
                #                (0, 0, {'product_id': 2, 'product_uom_qty': 2, 'price_unit': 100})],
                'date_order': object['fecha'],
                # 'pricelist_id': 1,
                # 'currency_id': 1,
                # 'team_id': 1
            })

        # Devolvemos un formulario vacio al presionar el botón
        view_form = self.env['ir.ui.view'].search([('name', '=', 'trip.stork.service.view.form')])
        return {
            "type": "ir.actions.act_window",
            "name": "WEB Service confirmation form",
            "res_model": "sale.order",
            "view_type": "form",
            "view_mode": "tree,form",
            "views": [(view_form.id, 'form')],
            "target": "self",
        }
