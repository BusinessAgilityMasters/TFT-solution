# -*- coding: utf-8 -*-
# from odoo import http


# class BamPartnerCreditcheck(http.Controller):
#     @http.route('/bam_partner_creditcheck/bam_partner_creditcheck/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bam_partner_creditcheck/bam_partner_creditcheck/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bam_partner_creditcheck.listing', {
#             'root': '/bam_partner_creditcheck/bam_partner_creditcheck',
#             'objects': http.request.env['bam_partner_creditcheck.bam_partner_creditcheck'].search([]),
#         })

#     @http.route('/bam_partner_creditcheck/bam_partner_creditcheck/objects/<model("bam_partner_creditcheck.bam_partner_creditcheck"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bam_partner_creditcheck.object', {
#             'object': obj
#         })
