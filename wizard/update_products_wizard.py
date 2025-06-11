# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
import logging
import datetime
from datetime import datetime
import openpyxl

import base64
import io
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_variant_id = fields.Many2one(store=True)

class BramaleaUpdateProductsWizard(models.TransientModel):
    _name = 'bramalea.update_products.wizard'
    _description = 'Update products and prices'

    file_ex = fields.Binary("File")
    type = fields.Char("Type")

    def update_products(self):
        file_data = base64.b64decode(self.file_ex)
        file_stream = io.BytesIO(file_data)

        # Load workbook with openpyxl
        workbook = openpyxl.load_workbook(file_stream, data_only=True)
        sheet = workbook.active  # or workbook['SheetName']

        count = 0
        skus = []
        skus_dic = {}
        product_dic = {}
        tire_brand_d = {}
        tire_type_d = {}
        sub_type_d = {}
        tread_type_d = {}
        width_d = {}
        aspect_ratio_d = {}
        rim_diameter_d = {}
        load_index_d = {}
        speed_rating_d = {}
        load_type_d = {}
        outside_diameter_d = {}
        side_wall_d = {}
        rim_width_min_d = {}
        rim_width_max_d = {}
        utqg_treadwear_d = {}
        utqg_traction_d = {}
        utqg_temperature_d = {}
        tread_depth_d = {}

        product_ids = self.env['product.template'].search([])
        for product in product_ids:
            barcode = product.barcode
            product_dic[barcode] = product

        logging.warning('product_dic')
        logging.warning(product_dic)
        
        tire_brand_ids = self.env['x_tire_brands'].search([])
        for b in tire_brand_ids:
            tire_brand_d[b.x_name] = b.id

        tire_type_ids = self.env['x_tire_type'].search([])
        for b in tire_type_ids:
            tire_type_d[b.x_name] = b.id

        tire_subtype_ids = self.env['x_tire_sub_type'].search([])
        for b in tire_subtype_ids:
            sub_type_d[b.x_name] = b.id

        tread_type_ids = self.env['x_tire_tread_type'].search([])
        for b in tread_type_ids:
            tread_type_d[b.x_name] = b.id
        logging.warning(tread_type_d)
        
        width_ids = self.env['x_tire_width'].search([])
        for b in width_ids:
            width_d[b.x_name] = b.id
    
        aspect_ratio_ids = self.env['x_tire_aspect_ratio'].search([])
        for b in aspect_ratio_ids:
            aspect_ratio_d[b.x_name] = b.id

        rim_diameter_ids = self.env['x_tire_rim_diameter'].search([])
        for b in rim_diameter_ids:
            rim_diameter_d[b.x_name] = b.id
            
        load_index_ids = self.env['x_tire_load_index'].search([])
        for b in load_index_ids:
            load_index_d[b.x_name] = b.id
            
        speed_rating_ids = self.env['x_tire_speed_rating'].search([])
        for b in speed_rating_ids:
            speed_rating_d[b.x_name] = b.id

        load_type_ids = self.env['x_tire_load_type'].search([])
        for b in load_type_ids:
            load_type_d[b.x_name] = b.id

        outside_diameter_ids = self.env['x_tire_outside_diamete'].search([])
        for b in outside_diameter_ids:
            outside_diameter_d[b.x_name] = b.id

        side_wall_ids = self.env['x_tire_side_wall'].search([])
        for b in side_wall_ids:
            side_wall_d[b.x_name] = b.id

        rim_width_min_ids = self.env['x_tire_rim_width_min'].search([])
        for b in rim_width_min_ids:
            rim_width_min_d[b.x_name] = b.id
        
        rim_width_max_ids = self.env['x_tire_rim_width_max'].search([])
        for b in rim_width_max_ids:
            rim_width_max_d[b.x_name] = b.id

        utqg_treadwear_ids = self.env['x_tire_utqg_treadwear'].search([])
        for b in utqg_treadwear_ids:
            utqg_treadwear_d[b.x_name] = b.id
            
        utqg_traction_ids = self.env['x_tire_utqg_traction'].search([])
        for b in utqg_traction_ids:
            utqg_traction_d[b.x_name] = b.id
            
        utqg_temperature_ids = self.env['x_tire_utqg_temperatur'].search([])
        for b in utqg_temperature_ids:
            utqg_temperature_d[b.x_name] = b.id
            
        tread_depth_ids = self.env['x_tire_tread_depth_in_'].search([])
        for b in tread_depth_ids:
            tread_depth_d[b.x_name] = b.id

        
        
        retail_price_id = 1
        retail_fleet_id = 7
        wholesale_a_id = 3
        wholesale_b_id = 4
        wholesale_c_id = 5
        wholesale_d_id = 6
        
        for row in sheet.iter_rows(min_row=1, values_only=True):  # Assuming header is in row 1
            logging.warning(count)
            if count >=1:
                sku = row[0]
                logging.warning(sku)
                skus.append(sku)
                skus_dic[sku] = row
                barcode = row[0]
                # number_format = barcode.number_format

                # if barcode is not None and isinstance(barcode, int):
                #     num_zeros = number_format.count('0')
                #     value_as_str = str(value).zfill(num_zeros)
                # else:
                #     value_as_str = str(barcode)

                # barcode = value_as_str
                            
                #tire_size = row[1] #falta
                name = row[2]
                brand = row[4]
                brand_id = tire_brand_d[brand] if brand in tire_brand_d else False
                product_line = row[5]
                tier = row[6]
                if name:
                    if type(tier) == str:
                        logging.warning("si es STR")
                        logging.warning(tier)
                        if "X" in str(tier):
                            tier = float(str(tier).replace("X", ""))
                        if "x" in str(tier):
                            tier = float(str(tier).replace("x", ""))
     
                    tire_type = row[7]
                    tire_type_id = tire_type_d[tire_type] if tire_type in tire_type_d else False
                    sub_type = row[8]
                    sub_type_id = sub_type_d[sub_type] if sub_type in sub_type_d else False
                    tread_type = row[9]
                    tread_type_id = tread_type_d[tread_type] if tread_type in tread_type_d else False
                    floatation = row[10] if row[9] else False
                    reference_size = row[11]
                    width = row[12]
                    width_id = False
                    if width:
                        if width in width_d:
                            width_id = width_d[width]
                        else:
                            width_c_id = self.env['x_tire_width'].create({'x_name': width})
                            width_id = width_c_id.id
                            width_d[width] = width_c_id.id
                        
                    aspect_ratio = row[13]
                    aspect_ratio_id = False
                    if aspect_ratio:
                        if aspect_ratio in aspect_ratio_d:
                            aspect_ratio_id = aspect_ratio_d[aspect_ratio]
                        else:
                            aspect_ratio_c_id = self.env['x_tire_aspect_ratio'].create({'x_name': aspect_ratio})
                            aspect_ratio_id = aspect_ratio_c_id.id
                            aspect_ratio_d[aspect_ratio] = aspect_ratio_c_id.id
                    
                    rim_diameter = row[14]
                    rim_diameter_id = False
                    if rim_diameter:
                        if rim_diameter in rim_diameter_d:
                            rim_diameter_id = rim_diameter_d[rim_diameter]
                        else:
                            rim_diameter_c_id = self.env['x_tire_rim_diameter'].create({'x_name': rim_diameter})
                            rim_diameter_id = rim_diameter_c_id.id
                            rim_diameter_d[rim_diameter] = rim_diameter_c_id.id
                        
                    load_index = row[15]
                    load_index_id = False
                    if load_index:
                        if load_index in load_index_d:
                            load_index_id = load_index_d[load_index]
                        else:
                            load_index_c_id = self.env['x_tire_load_index'].create({'x_name': load_index})
                            load_index_id = load_index_c_id.id
                            load_index_d[load_index] = load_index_c_id.id
                    
                    speed_rating = row[16]
                    speed_rating_id = False
                    if speed_rating:
                        if speed_rating in speed_rating_d:
                            speed_rating_id = speed_rating_d[speed_rating]
                        else:
                            speed_rating_c_id = self.env['x_tire_speed_rating'].create({'x_name': speed_rating})
                            speed_rating_id = speed_rating_c_id.id
                            speed_rating_d[speed_rating] =  speed_rating_c_id.id
                        
                    load_type = row[17]
                    load_type_id = False
                    if load_type:
                        if load_type in load_type_d:
                            load_type_id = load_type_d[load_type]
                        else:
                            load_type_c_id = self.env['x_tire_load_type'].create({'x_name': load_type})
                            load_type_id = load_type_c_id.id
                            load_type_d[load_type] = load_type_c_id.id
        
                    
                    studded_cd = row[17] #falta
                    pms = row[18] if row[18] else False
                    run_flat = ("RUNFLAT" if row[19] == "RUN FLAT" else  row[19]) if row[19] else ''
                    
                    msrp = row[30]
                    if type(msrp) == str:
                        if "," in msrp:
                            msrp = float(msrp.replace(",", ""))
    
                    
                    cost = row[31]
                    if type(cost) == str:
                        if "," in cost:
                            cost = float(cost.replace(",", ""))

                    outside_diameter = row[21]
                    outside_diameter_id = False
                    if outside_diameter:
                        if outside_diameter in outside_diameter_d:
                            outside_diameter_id = outside_diameter_d[outside_diameter]
                        else:
                            outside_diameter_c_id = self.env['x_tire_outside_diamete'].create({'x_name': outside_diameter})
                            outside_diameter_id = outside_diameter_c_id.id
                            outside_diameter_d[rim_diameter] = outside_diameter_c_id.id
                            
                    side_wall = row[22]
                    side_wall_id = False
                    if side_wall:
                        if side_wall in side_wall_d:
                            side_wall_id = side_wall_d[side_wall]
                        else:
                            side_wall_c_id = self.env['x_tire_side_wall'].create({'x_name': side_wall})
                            side_wall_id = side_wall_c_id.id
                            side_wall_d[side_wall] = side_wall_c_id.id

                    rim_width_min = row[23]
                    rim_width_min_id = False
                    if rim_width_min:
                        if rim_width_min in rim_width_min_d:
                            rim_width_min_id = rim_width_min_d[rim_width_min]
                        else:
                            rim_width_min_c_id = self.env['x_tire_rim_width_min'].create({'x_name': rim_width_min})
                            rim_width_min_id = rim_width_min_c_id.id
                            rim_width_min_d[rim_width_min] = rim_width_min_c_id.id

                    rim_width_max = row[24]
                    rim_width_max_id = False
                    if rim_width_max:
                        if rim_width_max in rim_width_max_d:
                            rim_width_max_id = rim_width_max_d[rim_width_max]
                        else:
                            rim_width_max_c_id = self.env['x_tire_rim_width_max'].create({'x_name': rim_width_max})
                            rim_width_max_id = rim_width_max_c_id.id
                            rim_width_max_d[rim_width_max] = rim_width_max_c_id.id

                    utqg_treadwear = row[25]
                    utqg_treadwear_id = False
                    if utqg_treadwear:
                        if utqg_treadwear in utqg_treadwear_d:
                            utqg_treadwear_id = utqg_treadwear_d[utqg_treadwear]
                        else:
                            utqg_treadwear_c_id = self.env['x_tire_utqg_treadwear'].create({'x_name': utqg_treadwear})
                            utqg_treadwear_id = utqg_treadwear_c_id.id
                            utqg_treadwear_d[utqg_treadwear] = utqg_treadwear_c_id.id

                    utqg_traction = row[26]
                    utqg_traction_id = False
                    if utqg_traction:
                        if utqg_traction in utqg_traction_d:
                            utqg_traction_id = utqg_traction_d[utqg_traction]
                        else:
                            utqg_traction_c_id = self.env['x_tire_utqg_traction'].create({'x_name': utqg_traction})
                            utqg_traction_id = utqg_traction_c_id.id
                            utqg_traction_d[utqg_traction] = utqg_traction_c_id.id

                    utqg_temperature = row[27]
                    utqg_temperature_id = False
                    if utqg_temperature:
                        if utqg_temperature in utqg_temperature_d:
                            utqg_temperature_id = utqg_temperature_d[utqg_temperature]
                        else:
                            utqg_temperature_c_id = self.env['x_tire_utqg_temperatur'].create({'x_name': utqg_temperature})
                            utqg_temperature_id = utqg_temperature_c_id.id
                            utqg_temperature_d[utqg_temperature] = utqg_temperature_c_id.id
                            
                    tread_depth = row[28]
                    tread_depth_id = False
                    if tread_depth:
                        if tread_depth in tread_depth_d:
                            tread_depth_id = tread_depth_d[tread_depth]
                        else:
                            tread_depth_c_id = self.env['x_tire_tread_depth_in_'].create({'x_name': tread_depth})
                            tread_depth_id = tread_depth_c_id.id
                            tread_depth_d[tread_depth] = tread_depth_c_id.id

                    warranty = row[29]
                    retail_pricelist = row[32]
                    retail_fleet = row[33]
                    wholesale_a = row[34]
                    wholesale_b = row[35]
                    wholesale_c = row[36]
                    wholesale_d = row[37]
                    homologation = row[20]
                    
                    # vendor = row[29]
                    # vendor_id = False

                    # if vendor:
                    #     partner_id = self.env['res.partner'].search([('name','=', vendor)])
                    #     vendor_id = partner_id
                    
                    if str(barcode) not in product_dic:
                        logging.warning(barcode)
    
                        p_dic = {
                            'name':name,
                            'barcode': barcode,
                            'list_price': msrp,
                            'standard_price': cost,
                            #'type': 'product',
                            'detailed_type': 'product',
                            #'default_code': tire_size,
                            'x_studio_inventory_type': 'Tire',
                            'categ_id': 48,
                            'x_studio_tire_reference_size': reference_size,
                            'x_studio_brand_tire': brand_id,
                            'x_studio_product_line_tire': product_line,
                            'x_studio_tire_tier': tier,
                            'x_studio_tire_type': tire_type_id,
                            'x_studio_tire_sub_type': sub_type_id,
                            'x_studio_tire_width': width_id,
                            'x_studio_tire_aspect_ratio': aspect_ratio_id,
                            'x_studio_tire_rim_diameter': rim_diameter_id,
                            'x_studio_tire_load_index': load_index_id,
                            'x_studio_tire_speed_rating': speed_rating_id,
                            'x_studio_tire_load_type': load_type_id,
                            'x_studio_tire_3pms': pms,
                            'x_studio_tire_run_flat': run_flat,
                            'x_studio_tire_homologation': homologation,
                            'x_studio_tire_outside_diameter_mm': outside_diameter_id,
                            'x_studio_tire_side_wall': side_wall_id,
                            'x_studio_tire_rim_width_min': rim_width_min_id,
                            'x_studio_tire_rim_width_max': rim_width_max_id,
                            'x_studio_tire_utqg_treadwear': utqg_treadwear_id,
                            'x_studio_tire_utqg_traction': utqg_traction_id,
                            'x_studio_tire_utqg_temperature': utqg_temperature_id,
                            'x_studio_tire_tread_depth_in_32nds': tread_depth_id,
                            'x_studio_warranty': warranty,
                        }
    
                        logging.warning(p_dic)
                        
                        new_product_id = self.env['product.template'].create(p_dic)
                        new_product_id.write({'standard_price': cost})
                        # if vendor_id:
                        #     supplier_info = self.env['product.supplierinfo'].create({''})
                        logging.warning(new_product_id)
                        if retail_pricelist != "#DIV/0!" and retail_pricelist is not None:
                            if float(retail_pricelist) > 0:
                                pricelist_retail = self.env['product.pricelist.item'].create({
                                    'product_tmpl_id': new_product_id.id,
                                    'fixed_price': float(retail_pricelist),
                                    'pricelist_id': retail_price_id,
                                })
                        if retail_fleet != "#DIV/0!" and retail_fleet is not None:
                            if float(retail_fleet) > 0:
                                pricelist_fleet = self.env['product.pricelist.item'].create({
                                    'product_tmpl_id': new_product_id.id,
                                    'fixed_price': float(retail_fleet),
                                    'pricelist_id': retail_fleet_id,
                                })

                        if wholesale_a != "#DIV/0!" and wholesale_a is not None:
                            if float(wholesale_a) > 0:
                                pricelist_retail_a = self.env['product.pricelist.item'].create({
                                    'product_tmpl_id': new_product_id.id,
                                    'fixed_price': float(wholesale_a),
                                    'pricelist_id': wholesale_a_id,
                                })
                        if wholesale_b != "#DIV/0!" and wholesale_b is not None:
                            if float(wholesale_b) > 0:
                                pricelist_retail_b = self.env['product.pricelist.item'].create({
                                    'product_tmpl_id': new_product_id.id,
                                    'fixed_price': float(wholesale_b),
                                    'pricelist_id': wholesale_b_id,
                                })
                                
                        if wholesale_c != "#DIV/0!" and wholesale_c is not None:
                            if float(wholesale_c) > 0:
                                pricelist_retail_b = self.env['product.pricelist.item'].create({
                                    'product_tmpl_id': new_product_id.id,
                                    'fixed_price': float(wholesale_c),
                                    'pricelist_id': wholesale_c_id,
                                })
                        if wholesale_d != "#DIV/0!" and wholesale_d is not None:
                            if float(wholesale_d) > 0:
                                pricelist_retail_c = self.env['product.pricelist.item'].create({
                                    'product_tmpl_id': new_product_id.id,
                                    'fixed_price': float(wholesale_d),
                                    'pricelist_id': wholesale_d_id,
                                })
                        _logger.info(f"No existe Row: {str(barcode)}")
                    else:
                        product = product_dic[str(barcode)]
                        
                        product_dic[str(barcode)].write({
                            'list_price': msrp,
                            'standard_price': cost,
                            'x_studio_tire_reference_size': reference_size,
                            #'default_code': tire_size,
                            'x_studio_tire_homologation': homologation,
                            'x_studio_tire_width': width_id,
                            'x_studio_tire_aspect_ratio': aspect_ratio_id,
                            'x_studio_tire_rim_diameter': rim_diameter_id,
                             'x_studio_tire_outside_diameter_mm': outside_diameter_id,
                            'x_studio_tire_side_wall': side_wall_id,
                            'x_studio_tire_rim_width_min': rim_width_min_id,
                            'x_studio_tire_rim_width_max': rim_width_max_id,
                            'x_studio_tire_utqg_treadwear': utqg_treadwear_id,
                            'x_studio_tire_utqg_traction': utqg_traction_id,
                            'x_studio_tire_utqg_temperature': utqg_temperature_id,
                            'x_studio_tire_tread_depth_in_32nds': tread_depth_id,
                            'x_studio_warranty': warranty,
                        })
    
                        if len(product.seller_ids) > 0:
                            product.seller_ids[0].price = cost
    
                        pricelist_retail = self.env['product.pricelist.item'].search([('pricelist_id','=', retail_price_id),('product_tmpl_id','=',product.id)])
                        if retail_pricelist != "#DIV/0!" and retail_pricelist is not None:
                            if len(pricelist_retail) > 0:
                                pricelist_retail.write({'fixed_price': retail_pricelist})
                                if len(pricelist_retail) > 1:
                                    pricelist_retail[1].unlink()
                            
                        # if str(barcode) == "200E1035":
                        #     _logger.info(f" este producto precio: {str(retail_pricelist)}")
                        #     _logger.info(f" retail retail: {str(pricelist_retail)}")

                        
                        pricelist_fleet = self.env['product.pricelist.item'].search([('pricelist_id','=', retail_fleet_id),('product_tmpl_id','=',product.id)])
                        if len(pricelist_fleet) > 0:
                            if retail_fleet != "#DIV/0!" and retail_fleet is not None:
                                pricelist_fleet.write({'fixed_price': retail_fleet})
                                if len(pricelist_fleet) > 1:
                                    pricelist_fleet[1].unlink()
                                
                        # if str(barcode) == "200E1035":
                        #     _logger.info(f" este producto precio: {str(retail_fleet)}")
                        #     _logger.info(f" pricelist fleet: {str(pricelist_fleet)}")
                        pricelist_retail_a = self.env['product.pricelist.item'].search([('pricelist_id','=', wholesale_a_id),('product_tmpl_id','=',product.id)])
                        
                        if len(pricelist_retail_a) > 0:
                            if wholesale_a != "#DIV/0!" and wholesale_a is not None:
                                pricelist_retail_a.write({'fixed_price': wholesale_a})
                                if len(pricelist_retail_a) > 1:
                                    pricelist_retail_a[1].unlink()
                            
                        pricelist_retail_b = self.env['product.pricelist.item'].search([('pricelist_id','=', wholesale_b_id),('product_tmpl_id','=',product.id)])
                        if len(pricelist_retail_b) > 0:
                            if wholesale_b != "#DIV/0!" and wholesale_b is not None:
                                pricelist_retail_b.write({'fixed_price': wholesale_b})
                                if len(pricelist_retail_b) > 1:
                                    pricelist_retail_b[1].unlink()
                            
                        pricelist_retail_c = self.env['product.pricelist.item'].search([('pricelist_id','=', wholesale_c_id),('product_tmpl_id','=',product.id)])
                        if len(pricelist_retail_c) > 0:
                            if wholesale_c != "#DIV/0!" and wholesale_c is not None:
                                pricelist_retail_c.write({'fixed_price': wholesale_c})
                                if len(pricelist_retail_c) > 1:
                                    pricelist_retail_c[1].unlink()
                            
                        pricelist_retail_d = self.env['product.pricelist.item'].search([('pricelist_id','=', wholesale_d_id),('product_tmpl_id','=',product.id)])
                        if len(pricelist_retail_d) > 0:
                            if wholesale_d != "#DIV/0!" and wholesale_d is not None:
                                pricelist_retail_d.write({'fixed_price': wholesale_d})
                                if len(pricelist_retail_d) > 1:
                                    pricelist_retail_d[1].unlink()
                        
                        _logger.info(f" existe Row: {str(barcode)}")
            count += 1
