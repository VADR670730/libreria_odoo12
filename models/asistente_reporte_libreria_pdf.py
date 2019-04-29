from odoo import models, api, fields
import time

class AsistenteReporteLibreria(models.TransientModel):
    _name = "libro.asistente_reporte_libreria"

    def _default_proveedor(self):
        if len(self.env.context.get('active_ids', [])) > 0:
            return self.env.context.get('active_ids')[0]
        else:
            return None

    proveedor_id = fields.Many2one('libro.proveedor',string="Proveedor", required=True, default=_default_proveedor)
    # proveedor_id = fields.Many2one('libro.proveedor',string="Proveedor", required=True)
    fecha_desde = fields.Date(string="Fecha Inicial", required=True, default=lambda self: time.strftime('%Y-%m-01'))
    fecha_hasta = fields.Date(string="Fecha hasta",required=True,default=lambda self: time.strftime('%Y-%m-%d'))

    @api.multi
    def print_report(self):
        data = {
            'ids': [],
            'proveedor_id': self.proveedor_id,
            'fecha_desde': self.fecha_desde,
            'fecha_hasta': self.fecha_hasta,
            'model': 'libro.asistente_reporte_libreria',
            'form': self.read()[0]
        }
        print(data)
        return self.env.ref('libreria_odoo12.action_reporte_libreria').report_action(self, data=data)

