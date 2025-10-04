# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[
            ('approved', 'Aprobada'),
            ('bom_customization', 'Customizar BOM'),
        ],
        ondelete={'approved': 'cascade', 'bom_customization': 'cascade'}
    )

    def action_approve_order(self):
        """Approve the sale order - transition to approved state"""
        self.ensure_one()
        _logger.info(f"Approving order {self.name} - transition to 'approved' state")
        
        if self.state in ['draft', 'sent']:
            self.state = 'approved'
            
            # Add a message to the chatter
            self.message_post(
                body="✅ La orden ha sido aprobada. Lista para customización de BOM.",
                message_type='notification'
            )
            
            return True
        else:
            raise UserError("Solo las cotizaciones en borrador o enviadas pueden ser aprobadas.")

    def action_customize_bom(self):
        """Move to BOM customization state"""
        self.ensure_one()
        _logger.info(f"Moving order {self.name} to BOM customization state")
        
        if self.state == 'approved':
            self.state = 'bom_customization'
            
            # Add a message to the chatter
            self.message_post(
                body="🔧 Orden movida a la fase de customización de BOM. Configure BOMs antes de la confirmación.",
                message_type='notification'
            )
            
            return True
        else:
            raise UserError("Solo las órdenes aprobadas pueden moverse a customización de BOM.")

    def action_confirm(self):
        """Override confirm to require approval and BOM customization"""
        # Check if this order has our custom states
        state_selection = dict(self._fields['state'].selection)
        has_approval_states = 'approved' in state_selection and 'bom_customization' in state_selection
        
        if has_approval_states:
            # Only apply our workflow rules if the order has our custom states
            if self.state == 'bom_customization':
                # Add a message before confirming
                self.message_post(
                    body="🚚 La orden está siendo confirmada. Creando entregas y órdenes de manufactura...",
                    message_type='notification'
                )
                
                # Temporarily change state to 'sent' so Odoo can confirm it
                original_state = self.state
                self.state = 'sent'
                
                try:
                    # Call the original confirm method
                    result = super().action_confirm()
                    
                    # Add success message
                    self.message_post(
                        body="✅ ¡Orden confirmada exitosamente!",
                        message_type='notification'
                    )
                    
                    return result
                except Exception as e:
                    # If confirmation fails, restore the original state
                    self.state = original_state
                    raise e
                
            elif self.state == 'approved':
                raise UserError(
                    "Esta orden está aprobada pero debe pasar por la fase de 'Customizar BOM' "
                    "antes de ser confirmada. Por favor, haga clic en el botón 'Customize BOM' primero."
                )
            elif self.state in ['draft', 'sent']:
                raise UserError(
                    "Esta orden debe ser aprobada y pasar por customización de BOM antes de ser confirmada. "
                    "Por favor, use el botón 'Approve Order' primero."
                )
        
        # For orders without approval workflow or in standard states, use standard behavior
        return super().action_confirm()

    def action_cancel(self):
        """Override cancel to handle approved and BOM customization states"""
        if self.state == 'approved':
            self.message_post(
                body="❌ Orden aprobada ha sido cancelada.",
                message_type='notification'
            )
        elif self.state == 'bom_customization':
            self.message_post(
                body="❌ Orden en customización de BOM ha sido cancelada.",
                message_type='notification'
            )
        return super().action_cancel()

    @api.model
    def _get_state_label(self, state):
        """Get human-readable label for state"""
        state_labels = {
            'draft': 'Cotización',
            'sent': 'Cotización Enviada',
            'approved': 'Aprobada',
            'bom_customization': 'Customización BOM',
            'sale': 'Orden de Venta',
            'done': 'Bloqueada',
            'cancel': 'Cancelada'
        }
        return state_labels.get(state, state.title())
