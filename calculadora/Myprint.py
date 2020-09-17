from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from uuid import uuid4,UUID
import io
from calculadora.models import ConsumoDeDispositivo
from calculadora.CalcularBateriaPanel import *
from calculadora.CalcularReporte import *
from calculadora.Calcular import *
class MyPrint:
    def __init__(self, buffer, pagesize,token,inversor,cantidades):
        
        self.cantidades = cantidades
        self.inversor = inversor
        self.buffer = buffer
        self.token = token
        self.datos = self.initComponents()
        self.panel = self.datos["TotalPanel"]
        self.bateria = self.datos["TotalBateria"]
        self.total = self.datos["resultadosDevices"] #self.total = total        
        self.ah = self.datos["ah"]
        self.panelCantidad = self.datos["panelCantidad"]
        
        self.setPageSize(pagesize)
        self.width, self.height = self.pagesize


    def initComponents(self):
        request = {            
            "inversor": self.inversor,
            "metros": self.cantidades,            
        }
        calcular = Calcular("", self.token)        
        ward = CalcularBateriaPanel("", self.token)
        ward.calcularPanelYbateria()
        reporte = CalcularReporte(ward,calcular.total())
        return reporte.getReporte(request)


    def setPageSize(self,pagesize):
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter

    def __getDoc(self):
        return SimpleDocTemplate(self.buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)
    def footer(self,canvas, doc):
        styles = getSampleStyleSheet()
        canvas.saveState()
        P = Paragraph("<i><b>Con los resultados obtenidos, para poder consultar el valor estimado de los equipos debe consultar con los diferentes proveedores en el mercado.</b></i>",
                    styles['Normal'])
        w, h = P.wrap(doc.width, doc.bottomMargin)
        P.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def printReport(self):        
        doc = self.__getDoc()
        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where the PDF generation happens. 
        # See the ReportLab documentation for the full list of functionality.
        elements.append(Paragraph("Reporte",styles['Title']))        
        elements.append(Paragraph("A continuación se muestra el total de equipos a utilizar en la implementacion del sistema fotovoltaico",styles['Italic']))
        elements.append(Spacer(1, 0.4*cm))
                                
        elements.append(self.datosTabla())
        elements.append(Paragraph("A continuación se detalla los equipos ingresados en el sistema que fueron considerados en el cálculo del consumo:",styles['Italic']))
        elements.append(Spacer(1, 0.7*cm))
        pdf = self.buffer.getvalue()
        elements.append(self.tabla())                    
        elements.append(Spacer(1, 2*cm))
        elements.append(Paragraph("Perfil de carga: {} KW/H".format(self.total),styles['Heading3']))
        
        doc.build(elements, onFirstPage=self.footer, onLaterPages=self.footer) 
        return pdf     
    def datosTabla(self):
        uso = ' a utilizar:'
        data = [
            ['Carga Máxima del dimensionamiento:', '{} KW'.format(self.total),''],
            ['La cantidad de paneles' + uso, str(self.panel),"{}W".format(self.panelCantidad) ],
            ['La cantidad de baterias' + uso,str(self.bateria),"{} Ah".format(self.ah)],
            ['Inversor OFF GRID' + uso, str(self.inversor),'' ],
            ['Cable solar 6mm color negro por metro',self.cantidades[0],''],
            ['Cable solar 6mm color rojo por metro',self.cantidades[0],''],
            ['Conector MC4 por par',self.cantidades[1],''],
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
            for device in self.datos["devices"]]
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
