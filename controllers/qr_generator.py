import qrcode
import os

class QRGenerator:
    @staticmethod
    def generar(codigo_producto):

        os.makedirs("assets/qrs", exist_ok=True)
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(codigo_producto)
        qr.make(fit=True)

        imagen = qr.make_image(fill_color="black", back_color="white")
        ruta = f"assets/qrs/{codigo_producto}.png"
        imagen.save(ruta)
        
        return ruta