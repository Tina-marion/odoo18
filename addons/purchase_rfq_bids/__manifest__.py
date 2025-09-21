{
    'name': 'Purchase RFQ Bids Management',
    'version': '18.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Enhanced RFQ management with multiple vendors and bid comparison',
    'author': 'Tina Marion',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/purchase_bid_views.xml',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
