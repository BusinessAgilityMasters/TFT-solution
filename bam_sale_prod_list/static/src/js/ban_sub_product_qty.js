odoo.define('bam_sale_prod_list.ban_sub_product_qty', function (require) {
    "use strict";

var ajax = require('web.ajax');
var Dialog = require('web.Dialog');
var ServicesMixin = require('web.ServicesMixin');
var VariantMixin = require('sale.VariantMixin');
var OptionalProductsModal = require('sale_product_configurator.OptionalProductsModal');

var OptionalProductsModal = OptionalProductsModal.include({
        events: _.extend({}, Dialog.prototype.events, VariantMixin.events, {
            'click .add_qty': '_onAddQty',
            'keypress .numericOnly': '_onnumericOnly',
            'click a.js_add, a.js_remove': '_onAddOrRemoveOption',
            'click button.js_add_cart_json': 'onClickAddCartJSON',
            'change .in_cart input.js_quantity': '_onChangeQuantity',
            'change .js_raw_price': '_computePriceTotal'
        }),

    _onAddQty: function (ev) {
        ev.preventDefault();
        var self = this;
        var $target = $(ev.currentTarget);
        var product_id = parseFloat($(ev.currentTarget.closest('tr')).find('.prod_main').val());
        var product_qty = parseFloat($(ev.currentTarget.closest('tr')).find('.qty_main').val());
        var product_qty_hidden = parseFloat($(ev.currentTarget.closest('tr')).find('.qty_hidden_main').val());
        var all_tr = $('.each_tr')
        var all_tr_sec = $('.each_tr')
        var all_tr_third = $('.each_tr')
        var all_tr_fourth = $('.each_tr')

        all_tr.each(function (index, value) {
            var data = $(value).find('.parent_prod_main').val()
            if(product_id == data){
                var qty = parseFloat($(value).find('.qty_hidden_main').val())
                var single_prod_qty = qty / product_qty_hidden
                var update_qty = single_prod_qty * product_qty
                $(value).find('.qty_main').val(update_qty)
                var product_id_sec = parseFloat($(value).find('.prod_main').val())
                all_tr_sec.each(function (index_sec, value_sec) {
                    var data_sec = parseFloat($(value_sec).find('.parent_prod_main').val())
                    if(product_id_sec == data_sec){
                        var qty_sec = parseFloat($(value_sec).find('.qty_hidden_main').val())
                        var update_qty_sec = qty_sec * product_qty
                        $(value_sec).find('.qty_main').val(update_qty_sec)
                        var product_id_third = parseFloat($(value_sec).find('.prod_main').val())
                        all_tr_third.each(function (index_third, value_third) {
                            var data_third = parseFloat($(value_third).find('.parent_prod_main').val())
                            if(product_id_third == data_third){
                                var qty_third = parseFloat($(value_third).find('.qty_hidden_main').val())
                                var update_qty_third = qty_third * product_qty
                                $(value_third).find('.qty_main').val(update_qty_third)
                                var product_id_fourth = parseFloat($(value_third).find('.prod_main').val())
                                all_tr_fourth.each(function (index_fourth, value_fourth) {
                                    var data_fourth = parseFloat($(value_fourth).find('.parent_prod_main').val())
                                    if(product_id_fourth == data_fourth){
                                        var qty_fourth = parseFloat($(value_fourth).find('.qty_hidden_main').val())
                                        var update_qty_fourth = qty_fourth * product_qty
                                        $(value_fourth).find('.qty_main').val(update_qty_fourth)
                                     }
                                })
                             }
                         })

                    }
                })
            }
        })
    },

    _onnumericOnly: function (ev) {
        if (String.fromCharCode(ev.keyCode).match(/[^0-9]/g)) return false;
    },

    _onAddOrRemoveOption: function (ev) {
        ev.preventDefault();
        var self = this;
        var $target = $(ev.currentTarget);
        var $modal = $target.parents('.oe_optional_products_modal');
        var $parent = $target.parents('.js_product:first');
        $parent.find("a.js_add, span.js_remove").toggleClass('d-none');
        $parent.find(".js_remove");

        var productTemplateId = $parent.find(".product_template_id").val();
        if ($target.hasClass('js_add')) {
            self._onAddOption($modal, $parent, productTemplateId);
        } else {
            self._onRemoveOption($modal, $parent);
        }

        self._computePriceTotal();
    },

    _onChangeQuantity: function (ev) {
        var $product = $(ev.target.closest('tr.js_product'));
        var qty = parseFloat($(ev.currentTarget).val());

        var uniqueId = $product[0].dataset.uniqueId;
        this.$el.find('tr.js_product:not(.in_cart)[data-parent-unique-id="' + uniqueId + '"] input[name="add_qty"]').each(function () {
            $(this).val(qty);
        });

        if (this._triggerPriceUpdateOnChangeQuantity()) {
            this.onChangeAddQuantity(ev);
        }
        if ($product.hasClass('main_product')) {
            this.rootProduct.quantity = qty;
        }
        this.trigger('update_quantity', this.rootProduct.quantity);
        this._computePriceTotal();
    },

    _computePriceTotal: function () {
        if (this.$modal.find('.js_price_total').length) {
            var price = 0;
            this.$modal.find('.js_product.in_cart').each(function () {
                var quantity = parseInt($(this).find('input[name="add_qty"]').first().val(), 10);
                price += parseFloat($(this).find('.js_raw_price').html()) * quantity;
            });

            this.$modal.find('.js_price_total .oe_currency_value').text(
                this._priceToStr(parseFloat(price))
            );
        }
    },

});

});