# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order'
    )
    
    def write(self, vals):
        print(f"WRITE PO vals {vals}")
        
        # Solo validamos cuando se modifican las líneas de la orden de compra
        if 'order_line' in vals:
            for operation in vals['order_line']:
                operation_type = operation[0]
                line_id = operation[1] if len(operation) > 1 else False
                
                # BLOQUEAR: Eliminación de líneas individuales con sale_order_line
                if operation_type == 2 and line_id:  # DELETE operation
                    line = self.env['purchase.order.line'].browse(line_id)
                    # Verifica si la línea de PO existe y está vinculada a una línea de SO
                    if line.exists() and line.sale_order_line:
                        raise UserError(
                            _("Cannot delete this purchase order line because it is linked to sales order line %s from sales order %s") % 
                            (line.sale_order_line.name, line.sale_order_line.order_id.name)
                        )
                
                # VALIDAR: Cambios en líneas con sale_order_line (UPDATE operation)
                elif operation_type == 1 and line_id and len(operation) >= 3:
                    values = operation[2]
                    line = self.env['purchase.order.line'].browse(line_id)
                    
                    if line.exists() and line.sale_order_line:
                        sale_line = line.sale_order_line
                        
                        # Validar producto
                        if 'product_id' in values and values['product_id'] != sale_line.product_id.id:
                            raise UserError(_("Product must match sales order line product"))
                        
                        # Validar cantidad
                        # Usamos product_uom_qty del sale_line porque es la cantidad "ordenada"
                        if 'product_qty' in values and values['product_qty'] != sale_line.product_uom_qty:
                            raise UserError(_("Quantity must match sales order quantity"))
                        
                        # Validar precio unitario (asume que la conversión de moneda y unidad ya ocurrió)
                        if 'price_unit' in values and values['price_unit'] != sale_line.price_unit:
                            raise UserError(_("Unit price must match sales order price"))
                
                # VALIDAR: Creación de nuevas líneas (CREATE operation)
                elif operation_type == 0 and len(operation) >= 3:
                    values = operation[2]

        return super(PurchaseOrder, self).write(vals)

    def unlink(self):
        """
        PERMITE eliminar órdenes de compra completas (incluyendo sus líneas)
        incluso si tienen sale_order_line.
        """
        # No hacemos validación - permitimos eliminar la PO completa
        return super(PurchaseOrder, self).unlink()