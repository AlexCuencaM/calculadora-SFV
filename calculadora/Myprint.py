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
    def __init__(self, buffer, pagesize,token,panel,bateria,total,inversor,ah,panelCantidad,cantidades):
        self.cantidades = cantidades

        self.buffer = buffer
        self.token = token
        self.panel = panel
        self.bateria = bateria
        self.total = total
        self.inversor = inversor
        self.ah = ah
        self.panelCantidad = panelCantidad
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
                                
        elements.append(self.datosTabla())
        elements.append(Paragraph("A continuación se detalla los equipos ingresados en el sistema que fueron considerados en el cálculo del consumo:",styles['Italic']))
        elements.append(Spacer(1, 0.7*cm))
        pdf = buffer.getvalue()
        elements.append(self.tabla())                    
        elements.append(Spacer(1, 2*cm))
        elements.append(Paragraph("Perfil de carga: {} KW/H".format(self.total),styles['Heading3']))
        
        doc.build(elements)                        
        return pdf     
    def datosTabla(self):
        uso = ' a utilizar:'
        data = [
                ['Carga Máxima del dimensionamiento:', '{} W'.format(self.total),''],
                ['La cantidad de paneles' + uso, str(self.panel),"{}W".format(self.panelCantidad) ],
                ['La cantidad de baterias' + uso,str(self.bateria),"{} Ah".format(self.ah)],
                ['Inversor OFF GRID' + uso, str(self.inversor),'' ],
                ['Cable solar 6mm color negro por metro',self.cantidades[0],''],
                ['Cable solar 6mm color rojo por metro',self.cantidades[1],''],
                ['Conector MC4 por par',self.cantidades[2],''],
                ['Conectores MC4 Triple Grado A',self.cantidades[3],''],
                ['Conectores MC4 Dobles en Y',self.cantidades[4],''],
                ['Estructura del panel',self.cantidades[5],''],
        ]
        data = Table(data, colWidths=[8 * cm, 3 * cm, 2 * cm, 4 * cm])  
        return data 

    def tabla(self):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = [['Nombre del equipo','Cantidad', 'Consumo KW/H'],]
        #Creamos una lista de tuplas que van a contener a las personas        
        detalles = [list((device.equipo.descripcion,
            str(device.equipo.cantidad),
            device.totalConsumoDiario))
            for device in ConsumoDeDispositivo.objects.filter(token=UUID(self.token,version=4))]
        for i in detalles:
            encabezados.append(i)        
        #Establecemos el tamaño de cada una de las columnas de la tabla
        tabla = Table(encabezados, colWidths=[10.0 * cm, 2.3 * cm, 3.0 * cm, 3 * cm])
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