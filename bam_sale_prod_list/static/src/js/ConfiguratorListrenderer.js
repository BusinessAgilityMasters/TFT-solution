odoo.define('bam_sale_prod_list.configurator_backend', function (require) {
// The goal of this file is to contain JS hacks related to allow
// configuring products on sale order.

"use strict";
var pyUtils = require('web.py_utils');
var core = require('web.core');
var _t = core._t;
var SectionAndNoteListRenderer = require('account.section_and_note_backend');
var ProductConfiguratorWidget = require('sale_product_configurator.product_configurator');

var ProductConfiguratorListRenderer = SectionAndNoteListRenderer.include({
    
    
    /**
     * Add support for product configurator
     *
     * @override
     * @private
     */
    _onAddRecord: function (ev) {
        
//        console.log("ProductConfiguratorListRenderer")
        
        // we don't want the browser to navigate to a the # url
        ev.preventDefault();

        // we don't want the click to cause other effects, such as unselecting
        // the row that we are creating, because it counts as a click on a tr
        ev.stopPropagation();

        // but we do want to unselect current row
        var self = this;
        var dataPointId = this.handle;
        this.unselectRow().then(function () {
            var context = ev.currentTarget.dataset.context;
            console.log("context>>>>>",context);

            var pricelistId = self._getPricelistId();
            if (context && pyUtils.py_eval(context).open_product_configurator){
                self._rpc({
                    model: 'ir.model.data',
                    method: 'xmlid_to_res_id',
                    kwargs: {xmlid: 'sale_product_configurator.sale_product_configurator_view_form'},
                }).then(function (res_id) {
                    self.do_action({
                        name: _t('Configure a product'),
                        type: 'ir.actions.act_window',
                        res_model: 'sale.product.configurator',
                        views: [[res_id, 'form']],
                        target: 'new',
                        context: {
                            'default_pricelist_id': pricelistId
                        }
                    },{on_close: function (products) {
//                            console.log("products>>>>>>>>.",products.mainProduct, products.options.length);
                            if (products && products !== 'special'){
                                self.trigger_up('add_record', {
                                    context: self._productsToRecords(products)[0] && [self._productsToRecords(products)[0]],
//                                    forceEditable: "bottom",
                                    allowWarning: true,
                                    onSuccess: function (){
//                                        self.unselectRow();
                                        console.log("products.options.length>>>>>>>",products.options.length)
                                        if (products.options.length > 0) {
                                            self.trigger_up('add_record', {
                                                context: self._productsToRecords(products.options) && [self._productsToRecords(products.options)],
                                                forceEditable: 'bottom',
                                                allowWarning: true,
                                                onSuccess: function () {
                                                    // Leave edit mode of one2many list.
                                                    self.unselectRow();
                                                }
                                            });
                                        }
                                    }
                                });
                            }
                        }
                    });
                });
            } else {
                self.trigger_up('add_record', {context: context && [context]}); // TODO write a test, the deferred was not considered
            }
        });
    },

    /**
     * Will try to get the pricelist_id value from the parent sale_order form
     *
     * @private
     * @returns {integer} pricelist_id's id
     */
    _getPricelistId: function () {
        var saleOrderForm = this.getParent() && this.getParent().getParent();
        var stateData = saleOrderForm && saleOrderForm.state && saleOrderForm.state.data;
        var pricelist_id = stateData.pricelist_id && stateData.pricelist_id.data && stateData.pricelist_id.data.id;

        return pricelist_id;
    },

    
    /**
     * Will map the products to appropriate record objects that are
     * ready for the default_get.
     *
     * @param {Array} products The products to transform into records
     *
     * @private
     */
    _productsToRecords: function (products) {
        var records = [];
        _.each(products, function (product) {
//            console.log('product>>>>>>>.',product)
            var record = {
                default_product_id: product.product_id,
                default_product_template_id: product.product_template_id,
                default_product_uom_qty: product.quantity,
            };

            if(product.x_sale_order_line_ids) {
                var default_x_sale_order_line_values = [];
                _.each(product.x_sale_order_line_ids, function (xline) {
                    default_x_sale_order_line_values.push(xline);
                });
                record['default_x_sale_order_line_ids'] = default_x_sale_order_line_values
            }

            if (product.no_variant_attribute_values) {
                var defaultProductNoVariantAttributeValues = [];
                _.each(product.no_variant_attribute_values, function (attributeValue) {
                        defaultProductNoVariantAttributeValues.push(
                            [4, parseInt(attributeValue.value)]
                        );
                });
                record['default_product_no_variant_attribute_value_ids']
                    = defaultProductNoVariantAttributeValues;
            }

            if (product.product_custom_attribute_values) {
                var defaultCustomAttributeValues = [];
                _.each(product.product_custom_attribute_values, function (attributeValue) {
                    defaultCustomAttributeValues.push(
                            [0, 0, {
                                custom_product_template_attribute_value_id: attributeValue.custom_product_template_attribute_value_id,
                                custom_value: attributeValue.custom_value
                            }]
                        );
                });
                record['default_product_custom_attribute_value_ids']
                    = defaultCustomAttributeValues;
            }

            records.push(record);
        });

//        console.log("records>>>>>>>>>",records)
        return records;
    }

});

return ProductConfiguratorListRenderer;

});