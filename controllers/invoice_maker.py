from reportlab.pdfgen import canvas
import os
from datetime import datetime

class InvoiceMaker:
    @staticmethod
    def generar_factura(nombre_producto, precio):
        # Aseguramos que la carpeta exista
        os.makedirs("assets/facturas", exist_ok=True)
        
        # Generamos un nombre único basado en la fecha y hora
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_pdf = f"assets/facturas/factura_{marca_tiempo}.pdf"
        
        # Dibujamos el PDF
        c = canvas.Canvas(ruta_pdf)
        
        # Coordenadas (x, y) desde la esquina inferior izquierda
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 800, "Factura de Venta - Gestor de Inventario")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 780, "-" * 60)
        c.drawString(100, 760, f"Fecha: {fecha_actual}")
        c.drawString(100, 740, f"Producto: {nombre_producto}")
        c.drawString(100, 720, f"Cantidad: 1")
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 690, f"TOTAL A PAGAR: ${precio}")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 670, "-" * 60)
        c.drawString(100, 650, "¡Gracias por su compra!")
        
        c.save()
        return ruta_pdf