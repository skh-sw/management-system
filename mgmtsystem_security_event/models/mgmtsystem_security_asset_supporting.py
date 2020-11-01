##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 - Present
#    Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models
from .mgmtsystem_security_event import _default_system_id


class SupportingAsset(models.Model):

    """Supporting Assets."""

    _name = "mgmtsystem.security.asset.supporting"
    _description = "Supporting Assets"

    name = fields.Char("Name")
    category_id = fields.Many2one("mgmtsystem.security.asset.category", "Category")
    primary_asset_ids = fields.Many2many("mgmtsystem.security.asset.primary", "mgmtsystem_security_asset_primary_rel", "supporting_asset_id", "primary_asset_id", "Primary Assets")
    system_id = fields.Many2one('mgmtsystem.system', 'System', required=True)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='system_id.company_id', readonly=True, store=True)

    _defaults = {
        'system_id': _default_system_id,
    }
