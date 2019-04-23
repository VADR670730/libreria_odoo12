from odoo import api, models

class ReporteLibreriaExcel(models.AbstractModel):
    _name = "report.libreria.reporte_libreria_excel"

    def lineas(self,datos):
        #registros = {}
        #
        # registros['correlativo'] = 0
        # registros['nombre'] = ''
        # registros['#Paginas'] = 0
        # registros['ISBN'] = ''
        # registros['fecha_ingreso'] = ''
        # registros['proveedor'] = None
        # registros['precio'] = 0

        libros = self.env['libreria.book'].search([
            ('proveedor','in',datos['proveedor']),
            ('date_order','<=',datos['fecha_hasta']),
            ('date_order','>=',datos['fecha_desde']),
        ],order='date_order')

        lineas = []
        correlativo = 0
        # precio = 0
        for lb in libros:
            correlativo +=1

            # if lb.price <= 0:
            #     precio = 0.00

            linea = {
                'correlativo': correlativo,
                'nombre':lb.name,
                'paginas':lb.pages,
                'isbn':lb.isbn,
                'fecha_ingreso':str(lb.date_order),
                'estado': lb.active,
                'precio': float(lb.price),
                'inventario':lb.inventario,
            }

            lineas.append(linea)

        return {'lineas':lineas}

    @api.model
    def _get_report_values(self,docids, data=None):
        return self.get_report_values(docids,data)

    @api.model
    def get_report_values(self,docids,data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids',[]))

        return {
            'doc_ids':self.ids,
            'doc_model':model,
            'data':data['form'],
            'docs':docs,
            'lineas':self.lineas,
        }