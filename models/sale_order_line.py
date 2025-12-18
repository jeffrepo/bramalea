# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string="Purchase Orders",
        copy=False,
    )

    def create_purchase(self):
        """Create ONE PO for the current line."""
        self.ensure_one()  # Asegura que solo se procese una línea

        print(f"ya solo la linea {self}")
        selected_supplier = False

        # Try to find first supplier
        
        if self.product_id and self.product_id.seller_ids:
            selected_supplier = self.product_id.seller_ids[0].partner_id

        if not selected_supplier:
            raise UserError(_("No supplier found in any product line."))

        print(f"supplier {selected_supplier}")
        # Prepare PO lines
        po_lines = []
        
        if self.product_id:
            seller = self.product_id.seller_ids.filtered(
                lambda s: s.partner_id == selected_supplier
            )

            po_lines.append((0, 0, {
                'product_id': self.product_id.id,
                'product_qty': self.product_uom_qty,
                'sale_order_line': self.id,
            }))

        # Create purchase order
        purchase_order = self.env['purchase.order'].create({
            'partner_id': selected_supplier.id,
            'origin': self.order_id.name,
            'order_line': po_lines,
            'sale_id': self.order_id.id,
        })

        print(f"purchase_order {purchase_order}")

        self.purchase_order_id = purchase_order.id

        # Retornar acción para mostrar la orden de compra
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order'),
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': purchase_order.id,
            'target': 'current',
        }
        