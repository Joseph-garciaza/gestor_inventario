import cv2
from pyzbar.pyzbar import decode

class Scanner:
    @staticmethod
    def iniciar_escaneo():
        # Abre la cámara web predeterminada
        cap = cv2.VideoCapture(0)
        codigo_detectado = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Busca códigos QR en la imagen actual de la cámara
            codigos = decode(frame)
            for codigo in codigos:
                codigo_detectado = codigo.data.decode('utf-8')
                break # Si encuentra uno, rompe el ciclo interno
            
            # Muestra la ventana de la cámara
            cv2.imshow("Escaneando... (Muestra el QR o presiona 'Q' para salir)", frame)

            # Si detectó un código o el usuario presiona 'Q', cierra la cámara
            if codigo_detectado or cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
        return codigo_detectado