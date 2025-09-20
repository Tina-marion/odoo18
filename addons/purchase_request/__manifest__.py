{
    "name": "Purchase Request",
    "version": "1.0",
    "summary": "Employees can send purchase requests to Procurement",
    "description": "Module for creating purchase requests, which generates purchase requests for procurement.",
    "category": "Purchases",
    "author": "Tina Marion Abwor",
    "depends": ["purchase"],
    "data": [
        "data/purchase_request_data.xml",
        "security/ir.model.access.csv",
        "views/purchase_request_views.xml"
    ],
    "installable": True,
    "application": False,
}
