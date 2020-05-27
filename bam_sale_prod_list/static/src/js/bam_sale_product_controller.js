odoo.define('bam_sale_prod_list.bam_sale_product_controller', function (require) {
"use strict";

var core = require('web.core');
var _t = core._t;
var FormController = require('web.FormController');
var OptionalProductsModal = require('sale_product_configurator.OptionalProductsModal');
var ProductConfiguratorFormController = require('sale_product_configurator.ProductConfiguratorFormController');

ProductConfiguratorFormController.include({

    _handleAdd: function () {
        var self = this;
        var $modal = this.$el;
        var productSelector = [
            'input[type="hidden"][name="product_id"]',
            'input[type="radio"][name="product_id"]:checked'
        ];

        var productId = parseInt($modal.find(productSelector.join(', ')).first().val(), 10);
        var productTemplateId = $modal.find('.product_template_id').val();
        this.renderer.selectOrCreateProduct(
            $modal,
            productId,
            productTemplateId,
            false
        ).then(function (productId) {
            $modal.find(productSelector.join(', ')).val(productId);

            var variantValues = self
                .renderer
                .getSelectedVariantValues($modal.find('.js_product'));

            var productCustomVariantValues = self
                .renderer
                .getCustomVariantValues($modal.find('.js_product'));

            var noVariantAttributeValues = self
                .renderer
                .getNoVariantAttributeValues($modal.find('.js_product'));

            self.rootProduct = {
                product_id: productId,
                product_template_id: parseInt(productTemplateId),
                quantity: parseFloat($modal.find('input[name="add_qty"]').val() || 1),
                variant_values: variantValues,
                product_custom_attribute_values: productCustomVariantValues,
                no_variant_attribute_values: noVariantAttributeValues
            };

//            if (self.renderer.state.context.configuratorMode === 'edit') {
//                // edit mode only takes care of main product
//                self._onAddRootProductOnly();
//                return;
//            }
            self.optionalProductsModal = new OptionalProductsModal($('body'), {
                rootProduct: self.rootProduct,
                pricelistId: self.renderer.pricelistId,
                okButtonText: _t('Confirm'),
                cancelButtonText: _t('Back'),
                title: _t('Configure'),
                context: self.initialState.context,
                previousModalHeight: self.$el.closest('.modal-content').height()
            }).open();

            self.optionalProductsModal.on('options_empty', null,
                // no optional products found for this product, only add the root product
                self._onAddRootProductOnly.bind(self));

            self.optionalProductsModal.on('update_quantity', null,
                self._onOptionsUpdateQuantity.bind(self));

            self.optionalProductsModal.on('confirm', null,
                self._onModalConfirm.bind(self));

            self.optionalProductsModal.on('closed', null,
                self._onModalClose.bind(self));
        });
    },

});

})