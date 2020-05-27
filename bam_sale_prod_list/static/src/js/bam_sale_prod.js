odoo.define('bam_sale_prod_list.bam_sale_prod', function (require) {
    "use strict";

var ajax = require('web.ajax');
var Dialog = require('web.Dialog');
var OptionalProduct = require('sale_product_configurator.OptionalProductsModal');
var ServicesMixin = require('web.ServicesMixin');
var VariantMixin = require('sale.VariantMixin');

var OptionalProductsModal = OptionalProduct.include({

    getSelectedProducts: function () {
        var bom_lines = [];
        this.$modal.find('.bom_lines tbody tr').each(function(){
            var r_val = {}
            r_val['level'] = parseInt($(this).find('td input[name="level"]').val());
            r_val['parent_product_id'] = parseInt($(this).find('td input[name="parent_product"]').val());
            r_val['product_id'] = parseInt( $(this).find('td input[name="product_id"]').val());
            r_val['qty'] = parseInt($(this).find('td input[name="qty"]').val());
            r_val['unit_price'] = parseFloat($(this).find('td input[name="unit_price"]').val());
            bom_lines.push([0,0,r_val]);
        })
        var self = this;
        var products = [this.rootProduct];
        this.$modal.find('.js_product.in_cart:not(.main_product)').each(function () {
            var $item = $(this);
            var quantity = parseInt($item.find('input[name="add_qty"]').val(), 10);
            var parentUniqueId = this.dataset.parentUniqueId;
            var uniqueId = this.dataset.uniqueId;
            var productCustomVariantValues = self.getCustomVariantValues($(this));
            var noVariantAttributeValues = self.getNoVariantAttributeValues($(this));
            products.push({
                'product_id': parseInt($item.find('input.product_id').val(), 10),
                'product_template_id': parseInt($item.find('input.product_template_id').val(), 10),
                'quantity': quantity,
                'parent_unique_id': parentUniqueId,
                'unique_id': uniqueId,
                'product_custom_attribute_values': productCustomVariantValues,
                'no_variant_attribute_values': noVariantAttributeValues,
                'x_sale_order_line_ids': bom_lines,
                'configurator': true
            });
        });
        products[0]['x_sale_order_line_ids'] = bom_lines
        return products;
    },

});

})