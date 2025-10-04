# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.model
    def _bom_find(self, products=None, **kwargs):
        """
        Override BOM search to prioritize flexible BOMs when in sale order context
        """
        # Handle both old and new method signatures
        product_tmpl = kwargs.get('product_tmpl')
        product = kwargs.get('product')
        
        # If products parameter is provided (new signature), extract product from it
        if products and not product and not product_tmpl:
            if hasattr(products, '__iter__'):
                product = products[0] if products else None
            else:
                product = products
        
        # First check if we're in a context where flexible BOM should be used
        sale_line_id = self.env.context.get('sale_line_id')
        flexible_bom_id = self.env.context.get('flexible_bom_id')
        
        if flexible_bom_id:
            flexible_bom = self.browse(flexible_bom_id)
            if flexible_bom.exists():
                _logger.info(f"🎯 Using flexible BOM from context: {flexible_bom.display_name}")
                return flexible_bom
        
        if sale_line_id:
            sale_line = self.env['sale.order.line'].browse(sale_line_id)
            if sale_line.exists() and hasattr(sale_line, 'flexible_bom_id') and sale_line.flexible_bom_id:
                # Check if the flexible BOM matches the product we're looking for
                flexible_bom = sale_line.flexible_bom_id
                if (product and flexible_bom.product_id == product) or \
                   (product_tmpl and flexible_bom.product_tmpl_id == product_tmpl):
                    _logger.info(f"🎯 Using flexible BOM from sale line: {flexible_bom.display_name}")
                    return flexible_bom
        
        # If no flexible BOM context, use standard logic
        try:
            if products is not None:
                # New signature with products parameter
                return super()._bom_find(products, **{k: v for k, v in kwargs.items() if k not in ['product_tmpl', 'product']})
            else:
                # Old signature - reconstruct products from individual parameters
                if product:
                    return super()._bom_find([product], **{k: v for k, v in kwargs.items() if k not in ['product_tmpl', 'product']})
                elif product_tmpl:
                    # For product template, we need to find products
                    products_for_tmpl = self.env['product.product'].search([('product_tmpl_id', '=', product_tmpl.id)])
                    if products_for_tmpl:
                        return super()._bom_find(products_for_tmpl, **{k: v for k, v in kwargs.items() if k not in ['product_tmpl', 'product']})
                    else:
                        return super()._bom_find([product_tmpl], **{k: v for k, v in kwargs.items() if k not in ['product_tmpl', 'product']})
                else:
                    # No products specified, return False
                    return self.browse()
        except TypeError:
            # Fallback: try old method signature
            return super()._bom_find(**kwargs)
