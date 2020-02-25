from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch,cm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from uuid import uuid4,UUID
import io
from calculadora.models import ConsumoDeDispositivo
class MyPrint:
    def __init__(self, buffer, pagesize,token):
        self.buffer = buffer
        self.token = token
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
    
    def printReport(self):

        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        elements.append(Paragraph("Reporte",styles['Title']))
        
        elements.append(Paragraph("Potencia en Wh/ día:",styles['Normal']))
        
        elements.append(Paragraph("La cantidad de paneles a utilizar: ",styles['Normal']))
        
        elements.append(Paragraph("La cantidad de baterias a utilizar: ",styles['Normal']))
        elements.append(Paragraph("Dispositivo:",styles['Normal']))
        pdf = buffer.getvalue()
        elements.append(self.tabla(pdf))            
        # elements.append(Paragraph('My User Names', styles['Heading1']))
        # for i, user in enumerate(users):
        #     elements.append(Paragraph(user.get_full_name(), styles['Normal']))
        doc.build(elements)                        
        return pdf     

    def tabla(self,pdf):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Nombre del equipo', 'Horas', 'Watts')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [list(encabezados),['c','fc','ff']]
        # detalles = [(device.equipo.equipo.descripcion,
        #     device.equipo.horas, device.equipo.watts)
        #     for device in ConsumoDeDispositivo.objects.filter(token=UUID(self.token,version=4))]
        
        #Establecemos el tamaño de cada una de las columnas de la tabla
        tabla = Table(detalles, colWidths=[5 * cm, 2 * cm, 2 * cm, 2 * cm])
        print(tabla)
        #Aplicamos estilos a las celdas de la tabla
        tabla.setStyle(TableStyle(
        [
                #La primera fila(encabezados) va a estar centrada
                #('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                #('GRID', (0, 0), (-1, -1), colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]
        ))
        
        return tabla