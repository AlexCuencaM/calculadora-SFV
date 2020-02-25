from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from uuid import uuid4,UUID
import io
from calculadora.models import ConsumoDeDispositivo
class MyPrint:
    def __init__(self, buffer, pagesize,token,panel,bateria,total,inversor):
        self.buffer = buffer
        self.token = token
        self.panel = panel
        self.bateria = bateria
        self.total = total
        self.inversor = inversor
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
        elements.append(Paragraph("A continuación se muestra el total de equipos a utilizar en la implementacion del sistema fovoltaico",styles['Italic']))
        elements.append(Spacer(1, 0.4*cm))
        
        elements.append(Paragraph("Potencia en Wh/ día: {} Watts".format(self.total),styles['Normal']))        
        elements.append(Paragraph("La cantidad de paneles a utilizar: {} Paneles".format(self.panel),styles['Normal']))        
        elements.append(Paragraph("La cantidad de baterias a utilizar: {} Baterias".format(self.bateria),styles['Normal']))                
        elements.append(Paragraph("Inversor Seleccionado: {}".format(self.inversor),styles['Normal']))
        elements.append(Spacer(1, 0.7*cm))
        pdf = buffer.getvalue()
        elements.append(self.tabla(pdf))                    
        doc.build(elements)                        
        return pdf     

    def tabla(self,pdf):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = [['Nombre del equipo', 'Horas', 'Watts'],]
        #Creamos una lista de tuplas que van a contener a las personas        
        detalles = [list((device.equipo.equipo.descripcion,
            str(device.equipo.horas), device.equipo.watts))
            for device in ConsumoDeDispositivo.objects.filter(token=UUID(self.token,version=4))]        
        for i in detalles:
            encabezados.append(i)        
        #Establecemos el tamaño de cada una de las columnas de la tabla
        tabla = Table(encabezados, colWidths=[8 * cm, 2.4 * cm, 2.4 * cm, 2.4 * cm])        
        #Aplicamos estilos a las celdas de la tabla
        tabla.setStyle(TableStyle(
        [
                #La primera fila(encabezados) va a estar centrada                
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1),1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]
        ))
        
        return tabla