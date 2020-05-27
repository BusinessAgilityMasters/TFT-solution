odoo.define('bam_sale_prod_list.ban_sale_product_config', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;

    var ProductConfiguratorWidget = require('sale_product_configurator.product_configurator');

ProductConfiguratorWidget.include({

//
//    events: _.extend({}, ProductConfiguratorWidget.prototype.events, {
//        'click .o_edit_orderline_button': '_onEditOrderLine'
//    }),
//
//     /**
//      * @override
//      */
//    _render: function () {
//        this._super.apply(this, arguments);
//        if (this.mode === 'edit' && this.value &&
//        (this._isConfigurableProduct() || this._isConfigurableLine())) {
//            this._addProductLinkButton();
//            this._addConfigurationEditButton();
//            this._addOrderLineEditButton();
//        } else if (this.mode === 'edit' && this.value) {
//            this._addProductLinkButton();
//            this._addOrderLineEditButton();
//            this.$('.o_edit_product_configuration').hide();
//        } else {
//            this.$('.o_external_button').hide();
//            this.$('.o_edit_product_configuration').hide();
//            this.$('.o_edit_orderline_button').hide();
//        }
//    },
//
//    /**
//     * Show edit order line button (in Edit Mode) after the product/product_template
//     */
//    _addOrderLineEditButton: function () {
//        var $inputDropdown = this.$('.o_input_dropdown');
//
//        if ($inputDropdown.length !== 0 &&
//            this.$('.o_edit_orderline_button').length === 0) {
//            var $editOrderLineButton = $('<button>', {
//                type: 'button',
//                class: 'fa fa-edit btn btn-default o_edit_orderline_button',
//                tabindex: '-1',
//                draggable: false,
//                'aria-label': _t('Edit Order Line'),
//                title: _t('Edit Order Line')
//            });
//
//            $inputDropdown.before($editOrderLineButton);
//        }
//    },
//
//    /**
//     * Triggered on click of the edit order line button.
//     * It is only shown in Edit mode,
//     *
//     * @private
//     */
//    _onEditOrderLine: function (ev) {
//        var self = this;
//        console.log(ev.currentTarget.dataset.context,"\nolself>>>>>>>", self)
//        
//        // we don't want the browser to navigate to a the # url
//        ev.preventDefault();
//
//        // we don't want the click to cause other effects, such as unselecting
//        // the row that we are creating, because it counts as a click on a tr
//        ev.stopPropagation();
//
//        // but we do want to unselect current row
////        var self = this;
////        this.unselectRow().then(function () {
////        self.trigger_up('add_record', {context: ev.currentTarget.dataset.context && [ev.currentTarget.dataset.context]}); // TODO write a test, the promise was not considered
////        });
//        
//        self.do_action({
//            name: _t('Edit Line'),
//            type: 'ir.actions.act_window',
//            res_model: 'sale.order.line',
//            res_id: self.recordData.id,
//            views: [[ false, 'form']],
//            target: 'new',
//            context: {
////                'default_pricelist_id': pricelistId,
//                'default_product_template_id': this.recordData.product_template_id.data.id,
//                default_sale_order_line_id: self.recordData.id,
//                default_pricelist_id: this._getPricelistId(),
//                default_product_template_attribute_value_ids: this._convertFromMany2Many(
//                    this.recordData.product_template_attribute_value_ids
//                ),
//                default_product_no_variant_attribute_value_ids: this._convertFromMany2Many(
//                    this.recordData.product_no_variant_attribute_value_ids
//                ),
//                default_product_custom_attribute_value_ids: this._convertFromOne2Many(
//                    this.recordData.product_custom_attribute_value_ids
//                ),
//                default_quantity: this.recordData.product_uom_qty
//            }
//        }, );
//    },
//
//    
//    _onTemplateChange: function (productTemplateId, dataPointId) {
//        var self = this;
//        var parentList = self.getParent();
//
//        return this._rpc({
//            model: 'product.template',
//            method: 'get_single_product_variant',
//            args: [
//                productTemplateId
//            ]
//        }).then(function (result) {
//            if (result.product_id && !result.has_optional_products) {
////                self.trigger_up('field_changed', {
////                    dataPointID: dataPointId,
////                    changes: {
////                        product_id: {id: result.product_id},
////                        product_custom_attribute_value_ids: {
////                            operation: 'DELETE_ALL'
////                        }
////                    },
////                });
//                console.log("vc adddddddddddd");
////                self.trigger_up('add_record', {
////                    view_type: 'form', dataPointID: dataPointId,
////                    context: [{default_product_id: result.product_id}],
//////                    forceEditable: 'bottom',
////                    allowWarning: true,
////                    onSuccess: function () {
////                        // Leave edit mode of one2many list.
////                        parentList.unselectRow();
////                    }
////                });
////                self.trigger_up('switch_view', {view_type: 'form', res_id: undefined, context: [{default_product_id: result.product_id}],});
//            } else {
//                return self._openConfigurator(result, productTemplateId, dataPointId);
//            }
//            // always returns true for the moment because no other configurator exists.
//        });
//    },
    
    


    _getMainProductChanges: function (mainProduct) {
        var result = {
            product_id: {id: mainProduct.product_id},
            product_template_id: {id: mainProduct.product_template_id},
            product_uom_qty: mainProduct.quantity,
            x_sale_order_line_ids: mainProduct.x_sale_order_line_ids,
        };


        var customAttributeValues = mainProduct.product_custom_attribute_values;
        var customValuesCommands = [{operation: 'DELETE_ALL'}];
        if (customAttributeValues && customAttributeValues.length !== 0) {
            _.each(customAttributeValues, function (customValue) {
                // FIXME awa: This could be optimized by adding a "disableDefaultGet" to avoid
                // having multiple default_get calls that are useless since we already
                // have all the default values locally.
                // However, this would mean a lot of changes in basic_model.js to handle
                // those "default_" values and set them on the various fields (text,o2m,m2m,...).
                // -> This is not considered as worth it right now.
                customValuesCommands.push({
                    operation: 'CREATE',
                    context: [{
                        default_custom_product_template_attribute_value_id: customValue.custom_product_template_attribute_value_id,
                        default_custom_value: customValue.custom_value
                    }]
                });
            });
        }

        result['product_custom_attribute_value_ids'] = {
            operation: 'MULTI',
            commands: customValuesCommands
        };


        var noVariantAttributeValues = mainProduct.no_variant_attribute_values;
        var noVariantCommands = [{operation: 'DELETE_ALL'}];
        if (noVariantAttributeValues && noVariantAttributeValues.length !== 0) {
            var resIds = _.map(noVariantAttributeValues, function (noVariantValue) {
                return {id: parseInt(noVariantValue.value)};
            });

            noVariantCommands.push({
                operation: 'ADD_M2M',
                ids: resIds
            });
        }

        result['product_no_variant_attribute_value_ids'] = {
            operation: 'MULTI',
            commands: noVariantCommands
        };
        return result;
    },

    _onEditProductConfiguration: function () {
        var sale_order_id = null;
        if (!this.recordData.is_configurable_product) {
            // if line should be edited by another configurator
            // or simply inline.
            this._super.apply(this, arguments);
            return;
        }
        if(this.recordData.id){
            sale_order_id = this.recordData.id
        }

        // If line has been set up through the product_configurator:
        this._openProductConfigurator({
                configuratorMode: 'edit',
                default_product_template_id: this.recordData.product_template_id.data.id,
                default_sale_order_line_id: sale_order_id,
                default_pricelist_id: this._getPricelistId(),
                default_product_template_attribute_value_ids: this._convertFromMany2Many(
                    this.recordData.product_template_attribute_value_ids
                ),
                default_product_no_variant_attribute_value_ids: this._convertFromMany2Many(
                    this.recordData.product_no_variant_attribute_value_ids
                ),
                default_product_custom_attribute_value_ids: this._convertFromOne2Many(
                    this.recordData.product_custom_attribute_value_ids
                ),
                default_quantity: this.recordData.product_uom_qty
            },
            this.dataPointID
        );
    },

})


});