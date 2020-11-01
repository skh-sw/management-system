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
from odoo.tools.translate import _


class EventControlLine(models.Model):

    """
    Event Control line.

    Event control lines are used inside the feared
    event model.
    """

    _name = "mgmtsystem.security.event.control"
    _description = "Feared Events - Control Lines"

    control_id = fields.Many2one("mgmtsystem.security.control", "Control")
    supporting_asset_id = fields.Many2one("mgmtsystem.security.asset.supporting", "Supporting Assets")
    security_event_id = fields.Many2one("mgmtsystem.security.event", "Feared Event")
    prevention = fields.Boolean("Prevention")
    protection = fields.Boolean("Protection")
    recovery = fields.Boolean("Recovery")
    system_id = fields.Many2one('mgmtsystem.system', 'System', related='security_event_id.system_id', store=True)
    

    def name_get(self):
        """
        The method gets the name of the objects referenced by ids.

        This method computes the name based on the controls and
        supporting_assets fields. It computes the name for each ids
        and can be extended by subclass.
        """
        if context is None:
            context = {}

        res = {}

        for obj in self:
            parts = [_("Events"),
                     obj.control_ids.name,
                     obj.supporting_asset_ids.name]
            obj.id.name = " - ".join(parts)

        return res
