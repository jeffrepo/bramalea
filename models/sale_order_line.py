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
        
    @api.onchange('price_unit')
    def _onchange_price_unit_restrict(self):
        """Bloquea cambios manuales en vista, pero NO los automáticos por cambio de producto."""
        if not self.env.user.has_group('bramalea.group_no_edit_price'):
            return

        if self._origin:
            # si el precio cambia y NO se cambió el producto → bloqueo
            if (
                self.price_unit != self._origin.price_unit
                and self.product_id == self._origin.product_id
            ):
                raise UserError("You are not allowed to manually modify Unit Price.")

    def write(self, vals):
        """Bloquea cambios en servidor, pero permite cambios por cambio de producto."""
        if 'price_unit' in vals:
            if self.env.user.has_group('bramalea.group_no_edit_price'):

                # permitir si el cambio viene junto a product_id
                if 'product_id' in vals:
                    return super().write(vals)

                # obtener valor anterior
                for line in self:
                    if vals['price_unit'] != line.price_unit:
                        raise UserError("You are not allowed to modify Unit Price.")

        return super().write(vals)
        
