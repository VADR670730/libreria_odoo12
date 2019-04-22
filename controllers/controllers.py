# -*- coding: utf-8 -*-
from odoo import http

# class Addons/libreria(http.Controller):
#     @http.route('/addons/libreria/addons/libreria/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/addons/libreria/addons/libreria/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('addons/libreria.listing', {
#             'root': '/addons/libreria/addons/libreria',
#             'objects': http.request.env['addons/libreria.addons/libreria'].search([]),
#         })

#     @http.route('/addons/libreria/addons/libreria/objects/<model("addons/libreria.addons/libreria"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('addons/libreria.object', {
#             'object': obj
#         })