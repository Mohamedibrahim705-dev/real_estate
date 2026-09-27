# -*- coding: utf-8 -*-
from odoo import api, models
from datetime import datetime, timedelta

class LeaseReportSummary(models.AbstractModel):
    _name = 'report.real_estate.report_lease_summary'
    _description = 'Lease Summary Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Override to add custom data to report context
        """
        leases = self.env['real_estate.lease'].browse(docids)

        six_months_ago = datetime.now().date() - timedelta(days=180)
        maintenance_costs = {}
        total_actual_costs = {}

        for lease in leases:
            costs = self.env['maintenance.request'].search([
                ('lease_id', '=', lease.id),
                ('completion_date', '>=', six_months_ago)
            ])
            maintenance_costs[lease.id] = sum(costs.mapped('actual_cost'))
            total_actual_costs[lease.id] = sum(lease.maintenance_ids.mapped('actual_cost'))
            
        payment_totals = {lease.id: 0.0 for lease in leases}
        payments = self.env['lease.payment'].search([
            ('lease_id', 'in', leases.ids),
        ])
        for payment in payments:
            payment_totals[payment.lease_id.id] += payment.total_amount
        
        return {
            'doc_ids': docids,
            'doc_model': 'real_estate.lease',
            'docs': leases,
            'maintenance_costs': maintenance_costs,
            'total_actual_costs': total_actual_costs,
            'payment_totals': payment_totals,
            'report_date': datetime.now(),
        }
