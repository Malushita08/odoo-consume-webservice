from odoo import models, fields
import requests


class kds_sale_order(models.Model):
    # Inherit fields from sale.order
    _inherit = ['sale.order']

    # Add the needed fields to save webservice data
    kds_serie_nota = fields.Char(string='kds_serie_nota')
    kds_no_nota = fields.Char(string='kds_no_nota')
    kds_estadodoc = fields.Char(string='kds_estadodoc')

    # Functions

    def call_web_service(self):
        # Consult the web service
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

        new_sale_orders = []

        for object in response.json():
            # Check if the client(res.partner) already exists and create it if not
            client = self.env['res.partner'].search([('kds_id_cliente', '=', object['id_cliente'])])
            if not client:
                client_data = {
                    'name': object['id_cliente'],
                    'kds_id_cliente': object['id_cliente'],
                    'kds_cliente_nuevo': object['ClienteNuevo'],
                    'kds_estado_cliente': object['EstadoCliente']
                }
                client = self.env['res.partner'].create(client_data)

            # Check if the product already exists and create it if not
            product = self.env['product.product'].search([('kds_id_producto', '=', object['id_producto'])])
            if not product:
                product_data = {
                    'name': object['id_producto'],
                    'kds_id_producto': object['id_producto'],
                    'detailed_type': 'product'
                }
                product = self.env['product.product'].create(product_data)

            # Check if the sale order already exists and create it if not
            sale_order = self.search([
                ('kds_serie_nota', '=', object['serie_nota']),
                ('kds_no_nota', '=', object['no_nota']),
            ])
            if not sale_order:
                sale_order_data = {
                    'partner_id': client.id,
                    'date_order': object['fecha'],
                    'kds_serie_nota': object['serie_nota'],
                    'kds_no_nota': object['no_nota'],
                    # 'pricelist_id': 1,
                    # 'currency_id': 1,
                    # 'team_id': 1
                }
                sale_order = self.create(sale_order_data)
                new_sale_orders.append(sale_order)

            # Check if the sale.order_line already exists and create it if not
            sale_order_line = self.env['sale.order.line'].search([
                ('order_id', '=', sale_order.id),
                ('product_id', '=', product.id)])
            if not sale_order_line:
                # Create sale.order_line
                sale_order_line_data = {
                    'order_id': sale_order.id,
                    'product_id': product.id,
                    'product_uom_qty': object['cantidad'],
                    'price_unit': object['precio'],
                    'price_total': object['monto']
                }
                sale_order_line = self.env['sale.order.line'].create(sale_order_line_data)

        # Confirm all the sale_orders and create their stock movement
        for sale_order in new_sale_orders:
            sale_order.action_confirm()
            for picking in sale_order.picking_ids:
                picking.action_assign()
                picking.action_confirm()
                for mv in picking.move_ids_without_package:
                    mv.quantity_done = mv.product_uom_qty
                picking.button_validate()

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
