# -*- coding: utf-8 -*-

from odoo import api, fields, models
import requests
import logging

_logger = logging.getLogger(__name__)

LARAVEL_BASE_URL = "https://your-laravel-site.com/api"

class ResPartner(models.Model):
    _inherit = 'res.partner'

    portal_status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        default='inactive',
        string="Portal Status",
        help="Set to Active to grant wholesale site access."
    )
    last_login = fields.Datetime(
        string="Last Login",
        compute="_compute_portal_info_from_api",
        store=False
    )
    failed_logins = fields.Integer(
        string="Failed Logins",
        compute="_compute_portal_info_from_api",
        store=False
    )
    wholesale_role = fields.Selection(
        [('admin', 'Admin'),
         ('purchaser', 'Purchaser'),
         ('accountant', 'Accountant')],
        string="Wholesale Role"
    )

    company_name = fields.Char('Company name', related='parent_id.name')

    # ===========================
    # FETCH LARAVEL PORTAL INFO
    # ===========================
    @api.depends('portal_status')
    def _compute_portal_info_from_api(self):
        for partner in self:
            partner.last_login = False
            partner.failed_logins = 0
            if partner.portal_status != 'active':
                continue
            try:
                api_url = f"{LARAVEL_BASE_URL}/portal-info/{partner.id}"
                response = requests.get(api_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    partner.last_login = data.get('last_login')
                    partner.failed_logins = data.get('failed_logins', 0)
                else:
                    _logger.warning("Laravel API returned %s for partner %s", response.status_code, partner.id)
            except Exception as e:
                _logger.error("Error fetching portal info for partner %s: %s", partner.id, e)

    # ===========================
    # HANDLE PORTAL STATUS CHANGE
    # ===========================
    def _call_laravel_portal_api(self, status):
        for partner in self:
            try:
                api_url = f"{LARAVEL_BASE_URL}/update-portal-status"
                payload = {
                    "contact_id": partner.id,
                    "status": status
                }
                response = requests.post(api_url, json=payload, timeout=5)
                if response.status_code != 200:
                    _logger.error("Failed to update portal status for %s: %s", partner.name, response.text)
            except Exception as e:
                _logger.error("Error calling Laravel API for %s: %s", partner.name, e)

    def write(self, vals):
        logging.warning(vals)
        if 'portal_status' in vals:
            for partner in self:
                if partner.portal_status != vals['portal_status']:
                    self._call_laravel_portal_api(vals['portal_status'])
        return super().write(vals)

    # ===========================
    # PASSWORD RESET BUTTON
    # ===========================
    def action_reset_password(self):
        for partner in self:
            try:
                api_url = f"{LARAVEL_BASE_URL}/reset-password"
                payload = {"contact_id": partner.id}
                response = requests.post(api_url, json=payload, timeout=5)
                if response.status_code != 200:
                    _logger.error("Failed to reset password for %s: %s", partner.name, response.text)
            except Exception as e:
                _logger.error("Error calling reset password for %s: %s", partner.name, e)