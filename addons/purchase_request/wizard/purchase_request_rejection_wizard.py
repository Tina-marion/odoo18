from odoo import models, fields, api

class PurchaseRequestRejectionWizard(models.TransientModel):
    _name = 'purchase.request.rejection.wizard'
    _description = 'Purchase Request Rejection Wizard'

    request_id = fields.Many2one('purchase.request', string='Purchase Request', required=True)
    rejection_reason = fields.Text(string='Rejection Reason', required=True)

    def action_reject_request(self):
        """Reject the purchase request with the provided reason"""
        self.request_id.write({
            'state': 'rejected',
            'rejection_reason': self.rejection_reason
        })
        return {'type': 'ir.actions.act_window_close'}