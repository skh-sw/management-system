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

from odoo import fields, models, api


def get_events_from_scenario_ids(self):
    scenario_ids = self.env['mgmtsystem.security.event.scenario'].search(
        cr, uid, [('vector_id', 'in', ids)])

    return self.env['mgmtsystem.security.event'].search(
        cr, uid, [('scenario_ids', 'in', scenario_ids)])


def get_events_from_event_scenario_ids(self):
    return self.env['mgmtsystem.security.event'].search(
        cr, uid, [('scenario_ids', 'in', ids)])


def _default_system_id(self):
    user = self.env.user

    company = user.company_id

    system_ids = self.env['mgmtsystem.system'].search([
            ('company_id', '=', company.id),
            ('type', '=', 'information_security'),
        ],
        limit=1)

    return system_ids


MULTI_FIELDS = {
    'method': True,
    'type': 'many2one',
    'multi': True,
    'store': {
        'mgmtsystem.security.vector': (
            get_events_from_scenario_ids, [
                'original_probability_id',
                'original_severity_id',
                'current_probability_id',
                'current_severity_id',
                'residual_probability_id',
                'residual_severity_id',
            ], 10),
        'mgmtsystem.security.event.scenario': (
            get_events_from_event_scenario_ids, [
                'vector_id'
            ], 10),
        'mgmtsystem.security.event': (
            lambda self, cr, uid, ids, c={}: ids, [
                'scenario_ids'
            ], 10),
    }
}


class FearedEvents(models.Model):

    """Feared Events."""

    _name = "mgmtsystem.security.event"
    _inherits = {'document.page': 'document_page_id'}
    _description = "Feared Events"

    @api.depends('scenario_ids', 'scenario_ids.vector_id', 'scenario_ids.vector_id.original_probability_id', 
                 'scenario_ids.vector_id.original_severity_id', 'scenario_ids.vector_id.current_probability_id',
                 'scenario_ids.vector_id.current_severity_id', 'scenario_ids.vector_id.residual_probability_id',
                 'scenario_ids.vector_id.residual_severity_id')
    def _compute_severity_and_probability(self, args=False):
        res = {}
        for event in self:
            fields = [
                'original_probability_id',
                'original_severity_id',
                'current_probability_id',
                'current_severity_id',
                'residual_probability_id',
                'residual_severity_id',
            ]

            event_fields = {
                field: False for field in fields
            }

            scenario_ids = [s.vector_id for s in event.scenario_ids]

            for field in fields:
                max_value = 0
                for scenario in scenario_ids:

                    record = getattr(scenario, field)

                    if record.value > max_value:
                        max_value = record.value
                        event_fields[field] = record.id
            for field, value in event_fields.Items():
                setattr(event, field, value)
        #return res

    system_id = fields.Many2one('mgmtsystem.system', 'System', required=True, default=_default_system_id)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='system_id.company_id', readonly=True)
    document_page_id = fields.Many2one("document.page", "Description", ondelete='cascade', required=True)
    display_content = fields.Text('Display Content')
    severity_id = fields.Many2one("mgmtsystem.severity", "Severity")
    scenario_ids = fields.One2many("mgmtsystem.security.event.scenario", "security_event_id", "Scenarios")
    control_ids = fields.One2many("mgmtsystem.security.event.control", "security_event_id", "Controls")
    confidentiality = fields.Boolean('Confidentiality')
    integrity = fields.Boolean('Integrity')
    availability = fields.Boolean('Availability')
    original_probability_id = fields.Many2one(comodel_name='mgmtsystem.probability', string='Original Probability', compute='_compute_severity_and_probability', store=True)
    #original_probability_id = fields.Function(_compute_severity_and_probability, string='Original Probability', relation='mgmtsystem.probability', **MULTI_FIELDS)
    original_severity_id = fields.Many2one(comodel_name='mgmtsystem.severity', string='Original Severity', compute='_compute_severity_and_probability', store=True)
    #original_severity_id = fields.Function(_compute_severity_and_probability, string='Original Severity', relation='mgmtsystem.severity', **MULTI_FIELDS)
    current_probability_id = fields.Many2one(comodel_name='mgmtsystem.probability', string='Current Probability', compute='_compute_severity_and_probability', store=True)
    #current_probability_id = fields.Function(_compute_severity_and_probability, string='Current Probability', relation='mgmtsystem.probability', **MULTI_FIELDS)
    current_severity_id = fields.Many2one(comodel_name='mgmtsystem.severity', string='Current Severity', compute='_compute_severity_and_probability', store=True)
    #'current_severity_id': fields.Function(_compute_severity_and_probability, string='Current Severity', relation='mgmtsystem.severity', **MULTI_FIELDS)
    residual_probability_id = fields.Many2one(comodel_name='mgmtsystem.probability', string='Residual Probability', compute='_compute_severity_and_probability', store=True)
    #'residual_probability_id': fields.Function(_compute_severity_and_probability, string='Residual Probability', relation='mgmtsystem.probability', **MULTI_FIELDS)
    residual_severity_id = fields.Many2one(comodel_name='mgmtsystem.severity', string='Residual Severity', compute='_compute_severity_and_probability', store=True)
    #'residual_severity_id': fields.Function(_compute_severity_and_probability, string='Residual Severity', relation='mgmtsystem.severity', **MULTI_FIELDS)
    

    def _default_parent_id(self):
        return self.env['ir.model.data'].get_object_reference(
            cr, uid, 'mgmtsystem_security_event',
            'document_page_group_feared_event')[1]

    _defaults = {
        'parent_id': _default_parent_id,
        'system_id': _default_system_id,
    }
