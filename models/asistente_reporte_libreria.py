from odoo import models, fields, api
import time
import xlwt
import base64
import io

class AsistenteReporteLibreriaExcel(models.TransientModel):
    _name = "libreria.asistente_reporte_libreria_excel"

    # def _default_proveedor(self):
    #     if len(self.env.context.get('active_ids',[]))>0:
    #         return self.env.context.get('active_ids')[0]
    #     else:
    #         return None

    # proveedor_id = fields.Many2one('libro.proveedor',string="Proveedor", required=True, default=_default_proveedor)
    proveedor_id = fields.Many2one('libro.proveedor',string="Proveedor", required=True)
    fecha_desde =fields.Date(string="Fecha Inicial", required=True, default=lambda self: time.strftime('%Y-%m-01'))
    fecha_hasta = fields.Date(string="Fecha hasta",required=True,default=lambda self: time.strftime('%Y-%m-01'))
    name = fields.Char('Nombre archivo', size=32)
    archivo = fields.Binary('Archivo', filters='.xls')

    @api.multi
    def print_report(self):
        data = {
            'ids': [],
            'model': 'libreria.asistente_reporte_libreria_excel',
            'form': self.read()[0]
        }
        return self.env.ref('libreria_odoo12.action_report_libreria_xls').report_action(self, data=data)

    def print_report_excel(self):
        for w in self:
            dict={}
            dict['fecha_hasta'] = w['fecha_hasta']
            dict['fecha_desde'] = w['fecha_desde']
            dict['proveedor'] = [w.proveedor_id.name]


            res = self.env['report.libreria.reporte_libreria_excel'].lineas(dict)
            lineas = res['lineas']
            # registros = res['registros']
            libro = xlwt.Workbook()
            hoja = libro.add_sheet('reporte')

            xlwt.add_palette_colour("custom_colour",0x21)
            libro.set_colour_RGB(0x21, 200, 200, 200)
            hoja.write(0,0,'Reporte de registros de libros')
            hoja.write(2,0,'Nombre de proveedor')
            hoja.write(2,1,w.proveedor_id[0].name)
            hoja.write(3,0,str(w.fecha_desde)+'al'+str(w.fecha_hasta))

            y = 5
            hoja.write(y,0,'Correlativo')
            hoja.write(y,1,'Nombre libro')
            hoja.write(y,2,'ISBN')
            hoja.write(y,3,'#Paginas')
            hoja.write(y,4,'Fecha')
            hoja.write(y,5,'Precio')
            hoja.write(y,6,'Inventario')

            for linea in lineas:
                y+=1
                hoja.write(y,0,linea['correlativo'])
                hoja.write(y,1,linea['nombre'])
                hoja.write(y,2,linea['isbn'])
                hoja.write(y,3,linea['paginas'])
                hoja.write(y,4,linea['fecha_ingreso'])
                hoja.write(y,5,linea['precio'])
                hoja.write(y,6,linea['inventario'])

            f = io.BytesIO()
            libro.save(f)
            datos = base64.b64encode(f.getvalue())
            self.write({'archivo':datos,'name':'libro_de_registros.xls'})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'libreria.asistente_reporte_libreria_excel',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }





