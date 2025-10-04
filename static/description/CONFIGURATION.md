# Configuration Guide - Sale Order Approval Workflow

## 🔧 Basic Configuration

### 1. User Permissions

#### Sales User (Basic)
```python
# Groups needed:
- sales_team.group_sale_salesman
```
**Capabilities:**
- Create sale orders
- Request approval
- View own orders

#### Sales Manager (Approval Authority)
```python
# Groups needed:
- sales_team.group_sale_manager
```
**Capabilities:**
- All sales user permissions
- Approve sale orders
- Access approval dashboard
- View all orders

#### Advanced Configuration
```xml
<!-- Custom record rule for approval restrictions -->
<record id="sale_order_approval_rule" model="ir.rule">
    <field name="name">Sale Order Approval Rule</field>
    <field name="model_id" ref="sale.model_sale_order"/>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
    <field name="domain_force">[('state', '=', 'draft')]</field>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="False"/>
    <field name="perm_unlink" eval="False"/>
</record>
```

### 2. Email Notifications (Optional Enhancement)

#### Automated Email for Approval Requests
```xml
<!-- Email template for approval notifications -->
<record id="email_template_approval_request" model="mail.template">
    <field name="name">Sale Order Approval Request</field>
    <field name="model_id" ref="sale.model_sale_order"/>
    <field name="subject">Approval Required: ${object.name}</field>
    <field name="body_html">
        <p>Dear Manager,</p>
        <p>Sale Order <strong>${object.name}</strong> requires your approval.</p>
        <p><strong>Customer:</strong> ${object.partner_id.name}</p>
        <p><strong>Amount:</strong> ${object.amount_total} ${object.currency_id.name}</p>
        <p><strong>Salesperson:</strong> ${object.user_id.name}</p>
        <p>Please review and approve in Odoo.</p>
    </field>
</record>
```

### 3. Custom Views (Advanced)

#### Add Approval Date Field
```python
# In models/sale_order.py
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    approval_date = fields.Datetime(
        string='Approval Date',
        readonly=True,
        help="Date when the order was approved"
    )
    
    approved_by = fields.Many2one(
        'res.users',
        string='Approved By',
        readonly=True,
        help="User who approved this order"
    )
```

#### Enhanced Form View
```xml
<!-- Add approval information to form view -->
<record id="view_order_form_approval_enhanced" model="ir.ui.view">
    <field name="name">sale.order.form.approval.enhanced</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='date_order']" position="after">
            <field name="approval_date" attrs="{'invisible': [('state', 'not in', ['approved', 'bom_customization', 'sale'])]}"/>
            <field name="approved_by" attrs="{'invisible': [('state', 'not in', ['approved', 'bom_customization', 'sale'])]}"/>
        </xpath>
    </field>
</record>
```

## 📊 Reporting Configuration

### 1. Approval Analytics Dashboard

#### Create Custom Dashboard
```xml
<!-- Approval analytics action -->
<record id="action_sale_approval_analytics" model="ir.actions.act_window">
    <field name="name">Approval Analytics</field>
    <field name="res_model">sale.order</field>
    <field name="view_mode">graph,pivot</field>
    <field name="domain">[('state', 'in', ['approved', 'bom_customization', 'sale'])]</field>
    <field name="context">{
        'group_by': ['user_id', 'approval_date:month'],
        'search_default_this_year': 1
    }</field>
</record>
```

### 2. Custom Filters

#### Pending Approvals Filter
```xml
<record id="filter_pending_approval" model="ir.filters">
    <field name="name">Pending Approval</field>
    <field name="model_id">sale.order</field>
    <field name="domain">[('state', 'in', ['draft', 'sent'])]</field>
    <field name="user_id" eval="False"/>
    <field name="is_default" eval="True"/>
</record>
```

## 🔐 Security Configuration

### 1. Access Rights

#### Basic Access Configuration
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sale_order_salesman,sale.order.salesman,sale.model_sale_order,sales_team.group_sale_salesman,1,1,1,0
access_sale_order_manager,sale.order.manager,sale.model_sale_order,sales_team.group_sale_manager,1,1,1,1
```

### 2. Record Rules

#### Approval Authority Rules
```xml
<!-- Sales users can only approve their own orders -->
<record id="sale_order_approval_salesman_rule" model="ir.rule">
    <field name="name">Sale Order: Salesman Approval</field>
    <field name="model_id" ref="sale.model_sale_order"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
</record>

<!-- Managers can approve all orders -->
<record id="sale_order_approval_manager_rule" model="ir.rule">
    <field name="name">Sale Order: Manager Approval</field>
    <field name="model_id" ref="sale.model_sale_order"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
</record>
```

## 🎯 Workflow Customization

### 1. Custom Approval Reasons

#### Add Approval Reason Field
```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    approval_reason = fields.Selection([
        ('standard', 'Standard Approval'),
        ('discount', 'Special Discount'),
        ('credit', 'Credit Check'),
        ('custom', 'Custom Requirements'),
        ('rush', 'Rush Order'),
    ], string='Approval Reason', help="Reason for approval")
```

### 2. Multi-Level Approval (Advanced)

#### Implementation Example
```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    approval_level = fields.Integer(default=0)
    required_approval_level = fields.Integer(compute='_compute_required_approval_level')
    
    @api.depends('amount_total')
    def _compute_required_approval_level(self):
        for order in self:
            if order.amount_total > 50000:
                order.required_approval_level = 2  # Senior manager
            elif order.amount_total > 10000:
                order.required_approval_level = 1  # Manager
            else:
                order.required_approval_level = 0  # Auto-approve
```

## 📱 Mobile Configuration

### 1. Mobile-Friendly Views

#### Simplified Mobile Form
```xml
<!-- Mobile-optimized form view -->
<record id="view_order_form_mobile" model="ir.ui.view">
    <field name="name">sale.order.form.mobile</field>
    <field name="model">sale.order</field>
    <field name="priority">20</field>
    <field name="arch" type="xml">
        <form>
            <header>
                <button name="action_approve" string="Approve" type="object" 
                        class="btn-success" attrs="{'invisible': [('state', 'not in', ['draft', 'sent'])]}"/>
            </header>
            <sheet>
                <div class="oe_title">
                    <h1><field name="name"/></h1>
                </div>
                <group>
                    <field name="partner_id"/>
                    <field name="amount_total"/>
                    <field name="state"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

## 🔄 Integration Examples

### 1. External Approval System

#### Webhook Integration
```python
def action_approve(self):
    result = super().action_approve()
    # Send to external system
    self._notify_external_approval_system()
    return result

def _notify_external_approval_system(self):
    webhook_url = self.env['ir.config_parameter'].get_param('approval.webhook.url')
    if webhook_url:
        requests.post(webhook_url, json={
            'order_id': self.id,
            'order_name': self.name,
            'amount': self.amount_total,
            'approved_by': self.env.user.id
        })
```

### 2. Credit Check Integration

#### Automatic Credit Verification
```python
@api.model
def action_approve(self):
    # Check credit limit before approval
    if not self._check_credit_limit():
        raise UserError("Credit limit exceeded. Cannot approve order.")
    return super().action_approve()

def _check_credit_limit(self):
    # Implement credit check logic
    return True
```

---

## 📞 Support

For advanced configuration assistance:
- GitHub Issues: Technical questions
- Documentation: Usage examples
- Professional Support: Custom implementations