# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_procurement_values(self, group_id=False):
        """Override to inject flexible BOM into procurement"""
        values = super()._prepare_procurement_values(group_id)
        
        # If this line has a flexible BOM, inject it into the procurement context
        if hasattr(self, 'flexible_bom_id') and self.flexible_bom_id:
            _logger.info(f"🔧 Injecting flexible BOM {self.flexible_bom_id.display_name} into procurement for line {self.id}")
            values['flexible_bom_id'] = self.flexible_bom_id.id
            # Override the standard BOM search
            values['bom_id'] = self.flexible_bom_id.id
        
        return values

    def _find_flexible_bom_for_product(self, product):
        """
        Find flexible BOM for a product in the current sale order.
        If no flexible BOM exists, fallback to base BOM.
        """
        # First, check if there's a flexible BOM for this product in the same sale order
        # Look for flexible BOMs that are linked to sale order lines in this order
        sale_lines_with_flexible_bom = self.env['sale.order.line'].search([
            ('order_id', '=', self.order_id.id),
            ('product_id', '=', product.id),
            ('flexible_bom_id', '!=', False)
        ])
        
        if sale_lines_with_flexible_bom:
            flexible_bom = sale_lines_with_flexible_bom[0].flexible_bom_id
            _logger.info(f"Found flexible BOM {flexible_bom.display_name} for product {product.display_name} in sale order")
            return flexible_bom
        
        # Alternative search: look for flexible BOMs created for this product recently
        flexible_bom = self.env['mrp.bom'].search([
            ('product_id', '=', product.id),
            ('is_flexible_bom', '=', True)
        ], order='create_date desc', limit=1)
        
        if flexible_bom:
            _logger.info(f"Found recent flexible BOM {flexible_bom.display_name} for product {product.display_name}")
            return flexible_bom
        
        # If no flexible BOM, use base BOM
        base_bom = self.env['mrp.bom']._bom_find(
            product,
            company_id=self.company_id.id,
            bom_type='phantom'  # Only look for KIT BOMs
        )
        
        if base_bom:
            _logger.info(f"Using base BOM {base_bom.display_name} for product {product.display_name}")
        
        return base_bom

    def _get_all_kit_components(self, product, bom, qty=1.0):
        """
        Recursively expand BOM to get all leaf components for KIT type BOMs.
        Returns a list of tuples (component_product, total_quantity)
        """
        components = []
        
        if not bom:
            _logger.info(f"⚠️ No BOM provided for product {product.display_name}, treating as leaf component")
            return [(product, qty)]
        
        # If BOM is not KIT type, return the product itself
        if bom.type != 'phantom':  # phantom = KIT in Odoo
            _logger.info(f"📋 BOM {bom.display_name} is not KIT type (type: {bom.type}), treating {product.display_name} as leaf")
            return [(product, qty)]
        
        _logger.info(f"🔧 Expanding KIT BOM {bom.display_name} for product {product.display_name} (qty: {qty})")
        
        for line in bom.bom_line_ids:
            component_product = line.product_id
            component_qty = line.product_qty * qty
            
            _logger.info(f"  📦 Component: {component_product.display_name} (qty: {component_qty})")
            
            # For sub-components, always use base BOM (since they weren't customized)
            component_bom = self.env['mrp.bom']._bom_find(
                component_product,
                company_id=self.company_id.id,
                bom_type='phantom'  # Only look for KIT BOMs
            )
            
            if component_bom and component_bom.type == 'phantom':
                _logger.info(f"    🔧 Component {component_product.display_name} has KIT BOM {component_bom.display_name}, expanding...")
                # Recursively expand this component's BOM
                sub_components = self._get_all_kit_components(
                    component_product, 
                    component_bom, 
                    component_qty
                )
                components.extend(sub_components)
            else:
                # This is a leaf component
                _logger.info(f"    ✅ {component_product.display_name} is leaf component (qty: {component_qty})")
                components.append((component_product, component_qty))
        
        _logger.info(f"🎯 Final components for {product.display_name}: {[(c[0].display_name, c[1]) for c in components]}")
        return components

    def _action_launch_stock_rule(self):
        """
        Override to handle KIT BOM expansion for deliveries.
        When a product has a KIT BOM with sub-KIT components, 
        create delivery for all leaf components instead.
        Uses flexible BOM if available, otherwise uses base BOM.
        """
        _logger.info(f"Launching stock rule for sale line {self.id} - Product: {self.product_id.display_name}")
        
        # First priority: Check if this sale line has a flexible BOM assigned
        bom = None
        if hasattr(self, 'flexible_bom_id') and self.flexible_bom_id:
            bom = self.flexible_bom_id
            _logger.info(f"✅ Using assigned flexible BOM: {bom.display_name} (ID: {bom.id})")
        else:
            # Fallback: Get the base BOM for this product
            bom = self.env['mrp.bom']._bom_find(
                self.product_id,
                company_id=self.company_id.id
            )
            if bom:
                _logger.info(f"⚠️ No flexible BOM found, using base BOM: {bom.display_name}")
            else:
                _logger.info(f"❌ No BOM found for product {self.product_id.display_name}")
        
        if bom and bom.type == 'phantom':  # KIT BOM
            _logger.info(f"🔧 Processing KIT BOM {bom.display_name} for product {self.product_id.display_name}")
            
            # Get all leaf components from the BOM (flexible or base)
            all_components = self._get_all_kit_components(
                self.product_id, 
                bom, 
                self.product_uom_qty
            )
            
            if all_components:
                _logger.info(f"📦 Expanded KIT to {len(all_components)} leaf components: {[c[0].display_name for c in all_components]}")
                
                # Create stock moves for each leaf component instead of the main product
                self._create_kit_stock_moves(all_components)
                return
            else:
                _logger.info("⚠️ No components found in KIT BOM")
        elif bom:
            _logger.info(f"📋 BOM {bom.display_name} is not a KIT (type: {bom.type}), using standard behavior")
        
        # If not a KIT or no BOM, use standard behavior
        _logger.info("🔄 Using standard stock rule behavior")
        return super()._action_launch_stock_rule()

    def _create_kit_stock_moves(self, components):
        """
        Create stock moves for KIT components.
        components: list of tuples (product, quantity)
        """
        _logger.info(f"Creating stock moves for {len(components)} KIT components")
        
        # Get the warehouse and location info
        warehouse = self.order_id._get_warehouse()
        if not warehouse:
            _logger.error("No warehouse found for sale order")
            return
        
        # Group components by product to avoid duplicates
        component_dict = {}
        for product, qty in components:
            if product.id in component_dict:
                component_dict[product.id]['qty'] += qty
            else:
                component_dict[product.id] = {
                    'product': product,
                    'qty': qty
                }
        
        # Create a delivery order for the components
        picking_vals = {
            'partner_id': self.order_id.partner_shipping_id.id,
            'picking_type_id': warehouse.out_type_id.id,
            'location_id': warehouse.out_type_id.default_location_src_id.id,
            'location_dest_id': self.order_id.partner_shipping_id.property_stock_customer.id,
            'origin': self.order_id.name,
            'move_type': 'direct',
        }
        
        picking = self.env['stock.picking'].create(picking_vals)
        _logger.info(f"Created picking {picking.name} for KIT components")
        
        # Create stock moves for each component
        for component_data in component_dict.values():
            product = component_data['product']
            qty = component_data['qty']
            
            move_vals = {
                'name': f"{self.order_id.name} - {product.display_name}",
                'product_id': product.id,
                'product_uom_qty': qty,
                'product_uom': product.uom_id.id,
                'picking_id': picking.id,
                'location_id': warehouse.out_type_id.default_location_src_id.id,
                'location_dest_id': self.order_id.partner_shipping_id.property_stock_customer.id,
                'sale_line_id': self.id,
                'origin': self.order_id.name,
            }
            
            move = self.env['stock.move'].create(move_vals)
            _logger.info(f"Created stock move for {product.display_name} - Qty: {qty}")
        
        # Confirm the picking to make it available
        picking.action_confirm()
        _logger.info(f"Confirmed picking {picking.name}")
