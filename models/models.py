# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.addons import decimal_precision as dp
import time 

# class addons/libreria(models.Model):
#     _name = 'addons/libreria.addons/libreria'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Proveedor(models.Model):
    _name = "libro.proveedor"

    name = fields.Char(string="Nombre")
    rubro = fields.Char(string="Rubro")

class Libreria(models.Model):
    _name = "libreria.book"
    _rec_name = "name"
    #date_order = fields.Datetime('Order Date', required=True, states=READONLY_STATES, index=True, copy=False, default=fields.Datetime.now,help="Depicts the date where the Quotation should be validated and converted into a purchase order.")
    STATES = [('inventario1','Inventario 1'),('inventario2','Inventario 2'),('inventario3','Inventario 3')]
    name = fields.Char(string="Nombre libro:")
    active = fields.Boolean(string="Activo:")
    image = fields.Binary(string="Imagen:")
    pages = fields.Integer(string="# paginas")
    isbn = fields.Char(string="ISBN", size=13)
    #date_order = fields.Datetime(string="Fecha ingreso",default=fields.Datetime.now,required=True)
    date_order = fields.Date(string="Fecha ingreso",default=str(datetime.today()),required=True)
    price = fields.Float(string="Precio", digits=(6,2),required=True,default=0.00)
    description = fields.Text(string="Descripcion")
    description2 = fields.Text(string="Descripcion")
    inventario = fields.Selection(string="Stock perteneciente",selection=STATES,default=STATES[0][0])
    proveedor = fields.Many2one(comodel_name="libro.proveedor",required=True)

class LibreriaVenta(models.Model):
    _name ="libreria.venta"

    READONLY_STATES = {
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    client = fields.Char(string="Cliente",required=True)
    partner_id = fields.Many2one("libro.proveedor",required=True, states=READONLY_STATES, change_default=True, track_visibility='always')
    date = fields.Datetime(string="Fecha",default=fields.Datetime.now,required=True)
    phone = fields.Char(string="Telefono")
    addres = fields.Char(string="Direccion",size=250)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES,
        default=lambda self: self.env.user.company_id.currency_id.id)
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    order_line = fields.One2many('libreria.venta.line','libreria_id',string="sell line",states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    tax = fields.Monetary(string="Impuesto",store=True, readonly=True)
    total = fields.Monetary(string="Total",store=True, readonly=True)
    notes = fields.Text('Terminos y condiciones')
    

class LibreriaVentaLine(models.Model):
    _name = "libreria.venta.line"

    libreria_id = fields.Many2one('libreria.venta', string="sell reference", index=True,required=True,ondelete='cascade')
    nameBook = fields.Many2one("libreria.book",string="Libros",required=True,change_default=True)
    price = fields.Float(string="Precio", digits=(6,2),required=True,default=0.00)
    quantity = fields.Float(string="Cantidad",digits=dp.get_precision('Product Unit of Measure'))
    subtotal = fields.Monetary(string="subtotal")
    tax_percentage = fields.Float(string="Total",digits=(8,2))
    state = fields.Selection(related='libreria_id.state', store=True, readonly=False)
    currency_id = fields.Many2one(related="libreria_id.currency_id", store=True, string='Currency', readonly=True)
    partner_id = fields.Many2one('res.partner', related='libreria_id.partner_id', string='Partner', readonly=True, store=True)

    @api.depends('quantity','price')
    def _compute_amount(self):
        for line in self:
            vals = line
    
    def _prepare_compute_all_values(self):
        self.ensure_one()

        return {
            'price':self.price,
            'currency_id':self.currency_id,
            'quantity':self.quantity,
            'nameBook':self.nameBook,
            'partner':self.libreria_id.partner_id,
        }

class AsistenteReporteLibreria(models.TransientModel):
    _name = "libro.asistente_reporte_libreria"

    # def _default_proveedor(self):
    #     if len(self.env.context.get('active_ids',[]))>0:
    #         return self.env.context.get('active_ids')[0]
    #     else:
    #         return None
        
    # proveedor_id = fields.Many2one('libro.proveedor',string="Proveedor", required=True, default=_default_proveedor)
    proveedor_id = fields.Many2one('libro.proveedor',string="Proveedor", required=True)
    fecha_desde =fields.Date(string="Fecha Inicial", required=True, default=lambda self: time.strftime('%Y-%m-01'))
    fecha_hasta = fields.Date(string="Fecha hasta",required=True,default=lambda self: time.strftime('%Y-%m-01'))

    @api.multi
    def print_report(self):
        data = {
            'ids':[],
            'model':'libro.asistente_reporte_libreria',
            'form':self.read()[0]
        }
        return self.env.ref('libreria_odoo12.action_reporte_libreria').report_action(self, data=data)

class ReporteLibreria(models.AbstractModel):
    _name = "report.libreria.reporte_libreria"

    def lineas(self,datos):
        lineas = []

        for linea in self.env['libreria.book'].search([('proveedor','=',datos['proveedor_id']),('date_order','<=',datos['fecha_desde']),('date_order','>=',datos['fecha_hasta'])],order='date_order'):
            detalle = {
                'fecha': str(linea.date_order),
                'name': linea.name,
                'page': linea.pages,
                'isbn': linea.isbn,
                'description': linea.description,
                'price': linea.price,
                'moneda': self.env.user.company_id.currency_id
            }
        
            lineas.append(detalle)
        return lineas
    
    @api.model
    def _get_report_values(self, docids,data = None):
        return self.get_report_values(docids,data)
    

    def get_report_values(self,docids,data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids',[]))

        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'lineas': self.lineas,
            'moneda': self.env.user.company_id.currency_id
        }




