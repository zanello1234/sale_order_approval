# Sale Order Approval Workflow

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo Version](https://img.shields.io/badge/Odoo-18.0-green.svg)](https://github.com/odoo/odoo/tree/18.0)

Professional approval workflow system for Odoo sale orders. Add mandatory approval step before order confirmation to improve control, compliance, and reduce errors.

## 🎯 Features

### ✅ Mandatory Approval Workflow
- **New "Approved" state** between quotation and confirmation
- **One-click approval** with dedicated "Approve" button
- **Controlled confirmation** - confirm only after approval
- **Visual indicators** showing approval status

### 📋 Enhanced User Experience
- **Clear workflow progression** with intuitive interface
- **Chatter integration** with automatic approval logging
- **Dedicated views** for approved orders
- **Role-based permissions** compatible with Odoo security

### 🔧 Technical Excellence
- **Minimal database impact** - simple state extension
- **Clean integration** with existing Odoo functionality
- **Performance optimized** - no system slowdown
- **Stable architecture** - easy to maintain and upgrade

## 🚀 Installation

1. Download the module
2. Place in your Odoo addons directory
3. Update the apps list
4. Install "Sale Order Approval Workflow"

## 📖 Usage

### Standard Workflow (Before)
```
Draft → Sent → Sale Order
```

### Enhanced Workflow (After)
```
Draft → Sent → Approved → Sale Order
```

### Step-by-Step Process

1. **Create Quotation** 📝
   - Create sale order as usual
   - Add products and configure pricing

2. **Send to Customer** 📧
   - Email quotation to customer
   - Customer confirms acceptance

3. **Approve Order** ✅
   - Click "Approve" button when ready
   - Order moves to "Approved" state
   - Action logged in chatter

4. **Confirm Sale** 🎯
   - "Confirm" button becomes available
   - Proceed with standard confirmation
   - Deliveries and MOs created as usual

## 🏭 Use Cases

### Manufacturing Companies
- **Quality Control**: Ensure all orders reviewed before production
- **Resource Planning**: Approve orders based on capacity
- **Cost Control**: Verify pricing and margins before commitment

### Service Providers
- **Resource Allocation**: Approve before assigning team members
- **Capacity Management**: Ensure availability before confirmation
- **Client Authorization**: Multiple approval levels for large projects

### B2B Sales
- **Enterprise Sales**: Formal approval for large orders
- **Credit Control**: Verify customer creditworthiness
- **Pricing Approval**: Authorize special pricing or discounts

### Regulated Industries
- **Compliance**: Meet regulatory approval requirements
- **Audit Trail**: Complete documentation of all approvals
- **Quality Assurance**: Mandatory review before fulfillment

## 👥 Benefits by Role

### Sales Representatives
- ✅ Clear process to follow
- ✅ Visual indicators of order status
- ✅ Automatic approval notifications

### Sales Managers
- ✅ Control over order authorization
- ✅ Overview of pending approvals
- ✅ Audit trail of all decisions

### Operations Teams
- ✅ Only approved orders reach production
- ✅ Reduced errors and rework
- ✅ Better resource planning

### Finance Teams
- ✅ Credit control integration
- ✅ Pricing approval workflow
- ✅ Complete audit documentation

## 🔒 Security & Permissions

The module respects Odoo's security framework:

- **User Groups**: Compatible with existing sales permissions
- **Role-Based Access**: Customize who can approve orders
- **Audit Trail**: All approval actions logged
- **Data Integrity**: No unauthorized order confirmations

## 📊 Views & Reports

### New Views Added
- **Approved Orders**: Dedicated list view for approved orders
- **Approval Dashboard**: Overview of approval status
- **Pending Approvals**: Orders waiting for approval

### Enhanced Existing Views
- **Sale Order Form**: Approval button and status indicators
- **Sale Order List**: Approval status column
- **Chatter**: Automatic approval logging

## 🔧 Technical Details

### Database Changes
- Extends `sale.order` model with approval state
- Minimal impact on existing data
- Clean upgrade path

### Dependencies
- `sale` (Odoo core sales module)
- No external dependencies
- No additional server requirements

### Performance
- Zero impact on system performance
- Efficient database queries
- Optimized for large datasets

## 🤝 Support & Contribution

### Getting Help
- Check documentation first
- Review existing issues on GitHub
- Contact support for enterprise needs

### Contributing
- Fork the repository
- Create feature branch
- Submit pull request with tests
- Follow coding standards

## 📄 License

This module is licensed under [LGPL v3](https://www.gnu.org/licenses/lgpl-3.0.en.html).

## 🏷️ Tags

`sales` `approval` `workflow` `control` `compliance` `authorization` `manufacturing` `b2b` `enterprise` `quality-control`

---

**Transform your sales process today with professional approval workflow!**
