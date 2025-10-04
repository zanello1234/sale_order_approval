{
    'name': 'Sale Order Approval Workflow',
    'version': '18.0.1.2.1',
    'summary': '✅ Professional approval workflow for sale orders - Mandatory approval before confirmation',
    'description': """
Sale Order Approval Workflow - Professional Sales Control
==========================================================

Transform your sales process with mandatory approval workflow. Ensure every sale order 
goes through proper authorization before confirmation, improving control, compliance, 
and reducing errors.

🎯 **Key Features**
===================

• **Mandatory Approval State**: New "Approved" state between quotation and confirmation
• **One-Click Approval**: Simple "Approve" button for authorized users
• **Controlled Confirmation**: Confirm button only available after approval
• **Visual Indicators**: Clear status progression with intuitive interface
• **Audit Trail**: Complete tracking of approval history in chatter

📋 **Enhanced Workflow**
========================

**Standard Odoo:** Draft → Sent → Sale Order
**With This Module:** Draft → Sent → **Approved** → Sale Order

1. **Create Quotation** - Standard quotation creation process
2. **Send to Customer** - Email quotation as usual
3. **Approve Order** ✅ - **NEW STEP** - Click "Approve" when ready
4. **Confirm Sale** - "Confirm" button becomes available after approval

💼 **Business Benefits**
========================

• **Quality Control**: Mandatory approval ensures order accuracy before production
• **Compliance**: Full audit trail for regulatory requirements
• **Error Reduction**: Prevent incorrect orders from reaching production/inventory
• **Authorization Control**: Clear separation between sales and approval authority
• **Better Oversight**: Managers can track all approvals in dedicated views

🏭 **Perfect For**
==================

• **Manufacturing Companies** - Control over production authorization
• **Service Providers** - Approval before resource allocation
• **B2B Sales Teams** - Enterprise-level approval processes
• **Regulated Industries** - Compliance and audit requirements
• **Multi-User Environments** - Clear authorization hierarchy

🔧 **Technical Excellence**
===========================

• **Minimal Database Impact**: Simple state field extension
• **Clean Integration**: Works seamlessly with existing Odoo functionality
• **No Complex Inheritance**: Stable and maintainable code
• **Performance Optimized**: No impact on system performance
• **Easy Upgrade**: Simple upgrade path for future versions

🚀 **Installation & Usage**
============================

1. **Install**: One-click installation from Apps menu
2. **Automatic**: Approval workflow activates immediately
3. **Intuitive**: Users can start using without training
4. **Compatible**: Works with all standard Odoo sales features

📊 **Reporting & Views**
========================

• **Approved Orders View**: Dedicated list of all approved orders
• **Status Tracking**: Clear visual indicators in list and form views
• **Chatter Integration**: All approval actions logged automatically
• **Dashboard Ready**: Status information available for custom dashboards

🔒 **Security & Permissions**
==============================

• **Role-Based**: Compatible with Odoo's user groups and permissions
• **Flexible**: Can be customized for specific approval hierarchies
• **Secure**: All actions properly logged and tracked
• **Auditable**: Complete history of all approval decisions

This module is essential for any business that needs professional sales order 
management with proper approval controls.
    """,
    'author': 'Zanello Solutions',
    'maintainer': 'Zanello Solutions',
    'website': 'https://github.com/zanello1234',
    'support': 'https://github.com/zanello1234/custom_bom_approval_flow',
    'category': 'Sales/Sales',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
        'views/sale_order_bom_customization_menu.xml',
    ],
    'demo': [],
    'images': [
        'static/description/banner.svg',
        'static/description/icon.svg',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
    'price': 0,
    'currency': 'EUR',
    'live_test_url': '',
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
}
