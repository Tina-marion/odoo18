from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    
    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True, default=lambda self: 'PR/')
    requester_id = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user)
    date_request = fields.Datetime(string='Request Date', default=fields.Datetime.now)
    line_ids = fields.One2many('purchase.request.line', 'request_id', string='Request Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('rfq_created', 'RFQ Created'),
        ('done', 'Done')
    ], string='Status', default='draft')
    rejection_reason = fields.Text(string='Rejection Reason')
    rfq_id = fields.Many2one('purchase.order', string='Generated RFQ', readonly=True)
    rfq_count = fields.Integer(string='RFQ Count', compute='_compute_rfq_count')

    def action_submit(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        return {
            'name': 'Reject Purchase Request',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.request.rejection.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_request_id': self.id}
        }

    def action_reset_to_draft(self):
        self.write({
            'state': 'draft',
            'rejection_reason': False
        })

    def action_done(self):
        self.state = 'done'

    def action_create_rfq(self):
        """Create an RFQ from the approved purchase request"""
        if self.state != 'approved':
            raise UserError('Only approved purchase requests can be converted to RFQ.')
        
        # Create the RFQ
        rfq_vals = {
            'partner_id': False,  # Will be set when vendors are assigned
            'state': 'draft',
            'order_line': [],
            'origin': self.name,  # Reference to the purchase request
            'notes': f'Generated from Purchase Request: {self.name}',
        }
        
        # Create order lines from request lines
        for line in self.line_ids:
            order_line_vals = {
                'product_id': line.product_id.id,
                'name': line.description or line.product_id.name,
                'product_qty': line.product_qty,
                'product_uom': line.uom_id.id,
                'price_unit': 0.0,  # To be filled by vendors
                'date_planned': fields.Datetime.now(),
            }
            rfq_vals['order_line'].append((0, 0, order_line_vals))
        
        # Create the RFQ
        rfq = self.env['purchase.order'].create(rfq_vals)
        
        # Update the purchase request
        self.write({
            'state': 'rfq_created',
            'rfq_id': rfq.id
        })
        
        # Return action to view the created RFQ
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generated RFQ',
            'res_model': 'purchase.order',
            'res_id': rfq.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_rfq(self):
        """View the generated RFQ"""
        if not self.rfq_id:
            return
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generated RFQ',
            'res_model': 'purchase.order',
            'res_id': self.rfq_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.depends('rfq_id')
    def _compute_rfq_count(self):
        for record in self:
            record.rfq_count = 1 if record.rfq_id else 0

    @api.model
    def create(self, vals):
        if vals.get('name', 'PR/') == 'PR/':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'PR/'
        return super(PurchaseRequest, self).create(vals)
