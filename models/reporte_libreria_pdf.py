from odoo import fields, api, models


class ReporteLibreria(models.AbstractModel):
    _name = "report.libreria.reporte_libreria"

    def lineas(self, datos):
        lineas = []

        for linea in self.env['libreria.book'].search([('proveedor','=',datos['proveedor_id'][0]),('date_order','<=',datos['fecha_desde']),('date_order','>=',datos['fecha_hasta'])],order='date_order'):
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
        return self.get_report_values(docids, data)

    @api.model
    def get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids', []))

        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'lineas': self.lineas,
            'moneda': self.env.user.company_id.currency_id,
        }
