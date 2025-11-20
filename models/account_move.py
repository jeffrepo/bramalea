# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    def write(self, vals):
        print(f"WRITE vals {vals}")
        
        # Solo validamos cuando se modifican las líneas de factura
        if 'invoice_line_ids' in vals:
            for operation in vals['invoice_line_ids']:
                operation_type = operation[0]
                line_id = operation[1] if len(operation) > 1 else False
                
                # BLOQUEAR: Eliminación de líneas individuales con sale_line_ids
                if operation_type == 2 and line_id:  # DELETE operation
                    line = self.env['account.move.line'].browse(line_id)
                    if line.exists() and line.sale_line_ids:
                        raise UserError(
                            _("Cannot delete this invoice line because it is linked to sales order %s") % 
                            line.sale_line_ids.order_id.name
                        )
                
                # VALIDAR: Cambios en líneas con sale_line_ids (UPDATE operation)
                elif operation_type == 1 and line_id and len(operation) >= 3:
                    values = operation[2]
                    line = self.env['account.move.line'].browse(line_id)
                    if line.exists() and line.sale_line_ids:
                        sale_line = line.sale_line_ids[0]
                        
                        # Validar producto
                        if 'product_id' in values and values['product_id'] != sale_line.product_id.id:
                            raise UserError(_("Product must match sales order product"))
                        
                        # Validar cantidad
                        if 'quantity' in values and values['quantity'] != sale_line.product_uom_qty:
                            raise UserError(_("Quantity must match sales order quantity"))
                        
                        # Validar precio
                        if 'price_unit' in values and values['price_unit'] != sale_line.price_unit:
                            raise UserError(_("Unit price must match sales order price"))
        
        return super(AccountMove, self).write(vals)

    def unlink(self):
        """
        PERMITE eliminar facturas completas (incluyendo sus líneas)
        incluso si tienen sale_line_ids
        """
        # No hacemos validación - permitimos eliminar la factura completa
        return super(AccountMove, self).unlink()