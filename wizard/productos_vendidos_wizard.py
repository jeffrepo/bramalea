# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
import logging
import datetime
from datetime import datetime
import openpyxl
import base64
from io import BytesIO
from odoo.exceptions import UserError

class BramaleaUpdateProductsWizard(models.TransientModel):
    _name = 'bramalea.update_products.wizard'

    file_ex = fields.Binary("File")

    def update_products(self):
        try:
            wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file_ex)), read_only=True)
            ws = wb.active
            for record in ws.iter_rows(min_row=3, max_row=None, min_col=None,max_col=None, values_only=True):
                logging.warning(recod[1])
        return True

