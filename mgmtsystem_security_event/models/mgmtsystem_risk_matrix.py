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
from .mgmtsystem_security_event import _default_system_id


class MgmtsystemRiskMatrix(models.TransientModel):

    """Category of Assets."""

    _name = "mgmtsystem.risk.matrix"
    _description = "Management System Risk Matrix"

    def get_matrix_types(self):
        return [
            ('original', _('Before applying any control')),
            ('current', _('With current controls')),
            ('residual', _('After applying the planned controls')),
        ]

    type = fields.Selection(get_matrix_types, type='char', string='Type', required=True)
    system_id = fields.Many2one('mgmtsystem.system', 'System', required=True, default=_default_system_id)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='system_id.company_id', readonly=True, store=True)

    _defaults = {
        'type': 'current',
        'system_id': _default_system_id,
    }

    def get_event_list(self, severity, probability):
        if isinstance(ids, (int, long)):
            ids = [ids]

        assert len(ids) == 1

        matrix = self.browse(ids[0])

        if matrix.type == 'original':
            return [
                e for e in matrix.get_events()
                if e.original_probability_id == probability and
                e.original_severity_id == severity
            ]

        elif matrix.type == 'current':
            return [
                e for e in matrix.get_events()
                if e.current_probability_id == probability and
                e.current_severity_id == severity
            ]

        else:
            return [
                e for e in matrix.get_events()
                if e.residual_probability_id == probability and
                e.residual_severity_id == severity
            ]

    def probability_name(self, probability):
        return "%s.%s" % (probability.value, _(probability.name))

    def severity_name(self, severity):
        return "%s.%s" % (severity.value, _(severity.name))

    def get_events(self):
        if isinstance(ids, (int, long)):
            ids = [ids]

        assert len(ids) == 1

        matrix = self.browse(ids[0])

        event_obj = self.env['mgmtsystem.security.event']

        event_ids = event_obj.search([('system_id', '=', matrix.system_id.id)], context=context)

        return event_ids

    def get_probabilities(self):
        prob_obj = self.env['mgmtsystem.probability']

        prob_ids = prob_obj.search(
            cr, uid, [('category', '=', 'security')],
            order='value')

        return prob_obj.browse(prob_ids)

    def get_severities(self):
        severity_obj = self.env['mgmtsystem.severity']

        severity_ids = severity_obj.search(
            cr, uid, [('category', '=', 'security')],
            order='value desc')

        return severity_obj.browse(severity_ids)

    def get_type(self):
        if isinstance(ids, (int, long)):
            ids = [ids]

        assert len(ids) == 1

        matrix = self.browse(ids[0])

        matrix_types = {
            t[0]: t[1] for t in
            self.get_matrix_types(context=context)
        }

        return matrix_types[matrix.type]

    def get_cell_color(self, severity, probability):
        level_obj = self.env['mgmtsystem.risk.matrix.level']
        level_ids = level_obj.search([
                ('severity_min', '<=', severity.value),
                ('severity_max', '>=', severity.value),
                ('probability_min', '<=', probability.value),
                ('probability_max', '>=', probability.value),
            ])

        if not level_ids:
            return '#B6D7A8'

        level = level_ids[0]

        return {
            'green': '#B6D7A8',
            'orange': '#F9CB9C',
            'red': '#EA9999',
        }[level.color]

    def print_report(self):
        datas = {
            'model': 'mgmtsystem.risk.matrix',
            'ids': ids,
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'mgmtsystem_security_event.risk_matrix_webkit',
            'datas': datas,
        }
