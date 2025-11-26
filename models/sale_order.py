# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_order_ids = fields.Many2many(
        comodel_name='purchase.order',
        string="Purchase Orders",
        copy=False,
    )

    # =====================================================
    # CREATE PURCHASE ORDER
    # =====================================================
    def create_purchase_order(self):
        """Create ONE PO based on the first supplier found."""
        for order in self:
            selected_supplier = False

            # Try to find first supplier
            for line in order.order_line:
                if line.product_id and line.product_id.seller_ids:
                    selected_supplier = line.product_id.seller_ids[0].partner_id
                    break

            if not selected_supplier:
                raise UserError(_("No supplier found in any product line."))

            # Prepare PO lines
            po_lines = []
            for line in order.order_line:
                if line.product_id:
                    seller = line.product_id.seller_ids.filtered(
                        lambda s: s.partner_id == selected_supplier
                    )

                    po_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'product_qty': line.product_uom_qty,
                        'sale_order_line': line.id,
                    }))

            # Create purchase order
            purchase_order = self.env['purchase.order'].create({
                'partner_id': selected_supplier.id,
                'origin': order.name,
                'order_line': po_lines,
                'sale_id': order.id,
            })

            order.purchase_order_ids = [(4, purchase_order.id)]

            return {
                'type': 'ir.actions.act_window',
                'name': _('Purchase Order'),
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': purchase_order.id,
            }
        
    def action_view_purchase_orders_list(self):
        self.ensure_one()

        action = self.env.ref("purchase.purchase_rfq").read()[0]

        action["views"] = [
            (self.env.ref("purchase.purchase_order_tree").id, "tree"),
            (self.env.ref("purchase.purchase_order_form").id, "form"),
        ]

        action["domain"] = [("id", "in", self.purchase_order_ids.ids)]
        action.pop("res_id", None)

        return action



