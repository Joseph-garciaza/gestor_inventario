import customtkinter as ctk
from tkinter import messagebox
from models.db_manager import DBManager
from controllers.qr_generator import QRGenerator
from views.scanner_window import Scanner
from controllers.inventory_logic import InventoryLogic
from controllers.invoice_maker import InvoiceMaker
from tkinter import messagebox, ttk

class MainWindow(ctk.CTk):
    
    def abrir_ventana_inventario(self):
        ventana_inv = ctk.CTkToplevel(self)
        ventana_inv.title("Inventario Actual")
        ventana_inv.geometry("700x400")
        ventana_inv.grab_set()

        ctk.CTkLabel(ventana_inv, text="Stock de Productos", font=("Arial", 20, "bold")).pack(pady=15)

        # Contenedor para la tabla
        frame_tabla = ctk.CTkFrame(ventana_inv)
        frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Configurar los colores de la tabla para que coincidan con el tema oscuro
        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        estilo.configure("Treeview.Heading", background="#1f538d", foreground="white", font=("Arial", 10, "bold"))
        estilo.map('Treeview', background=[('selected', '#14375e')])

        # Crear la estructura de la tabla
        columnas = ("Codigo", "Nombre", "Precio", "Cantidad")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        # Asignar los nombres a las cabeceras
        tabla.heading("Codigo", text="Código")
        tabla.heading("Nombre", text="Nombre del Producto")
        tabla.heading("Precio", text="Precio ($)")
        tabla.heading("Cantidad", text="Stock Disponible")

        # Ajustar el ancho de las columnas
        tabla.column("Codigo", width=100, anchor="center")
        tabla.column("Nombre", width=250, anchor="w")
        tabla.column("Precio", width=100, anchor="center")
        tabla.column("Cantidad", width=120, anchor="center")

        tabla.pack(fill="both", expand=True)

        # Llenar la tabla consultando la base de datos
        logic = InventoryLogic()
        productos = logic.obtener_todos()
        
        for p in productos:
            # p contiene: (codigo, nombre, precio, cantidad)
            tabla.insert("", "end", values=(p[0], p[1], f"${p[2]:.2f}", p[3]))
            
    def __init__(self):
        super().__init__()

        self.db = DBManager()

        self.title("Gestor de Inventario")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.titulo = ctk.CTkLabel(self, text="Gestor de Inventario", font=("Arial", 28, "bold"))
        self.titulo.pack(pady=40)

        self.btn_vender = ctk.CTkButton(self, text="Escanear y Vender", width=200, height=40, command=self.procesar_venta)
        self.btn_vender.pack(pady=10)

        self.btn_agregar = ctk.CTkButton(self, text="Agregar Producto Nuevo", width=200, height=40, command=self.abrir_ventana_agregar)
        self.btn_agregar.pack(pady=10)

# Cambia esta línea:
        self.btn_inventario = ctk.CTkButton(self, text="Ver Inventario", width=200, height=40, command=self.abrir_ventana_inventario)
        self.btn_inventario.pack(pady=10)
        
    def abrir_ventana_agregar(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Nuevo Producto")
        ventana.geometry("400x450")
        ventana.grab_set() 

        ctk.CTkLabel(ventana, text="Código Único (Ej: PROD-01):").pack(pady=(20, 5))
        entry_codigo = ctk.CTkEntry(ventana, width=250)
        entry_codigo.pack(pady=5)

        ctk.CTkLabel(ventana, text="Nombre del Producto:").pack(pady=5)
        entry_nombre = ctk.CTkEntry(ventana, width=250)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(ventana, text="Precio ($):").pack(pady=5)
        entry_precio = ctk.CTkEntry(ventana, width=250)
        entry_precio.pack(pady=5)

        ctk.CTkLabel(ventana, text="Cantidad Inicial:").pack(pady=5)
        entry_cantidad = ctk.CTkEntry(ventana, width=250)
        entry_cantidad.pack(pady=5)

        def guardar_producto():
            codigo = entry_codigo.get().strip()
            nombre = entry_nombre.get().strip()
            
            if not codigo or not nombre:
                messagebox.showerror("Error", "El código y el nombre son obligatorios.")
                return

            try:
                precio = float(entry_precio.get())
                cantidad = int(entry_cantidad.get())
                
                exito, mensaje = self.db.agregar_producto(codigo, nombre, precio, cantidad)
                
                if exito:
                    QRGenerator.generar(codigo)
                    messagebox.showinfo("Éxito", f"{mensaje}\nEl QR se ha guardado en la carpeta assets/qrs.")
                    ventana.destroy()
                else:
                    messagebox.showwarning("Atención", mensaje)

            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número decimal y la cantidad un número entero.")

        ctk.CTkButton(ventana, text="Guardar e Imprimir QR", command=guardar_producto, fg_color="green", hover_color="darkgreen").pack(pady=30)

    def procesar_venta(self):
        codigo = Scanner.iniciar_escaneo()
        
        if codigo:
            logic = InventoryLogic()
            producto = logic.buscar_producto(codigo)
            
            if producto:
                nombre = producto[1]
                precio = producto[2]
                stock_actual = producto[3]
                
                if stock_actual > 0:
                    logic.descontar_stock(codigo, 1)
                    ruta_factura = InvoiceMaker.generar_factura(nombre, precio)
                    messagebox.showinfo("Venta Exitosa", f"Se descontó 1 unidad de:\n{nombre}\nPrecio cobrado: ${precio}\n\nFactura guardada en:\n{ruta_factura}")
                else:
                    messagebox.showwarning("Sin Stock", f"El producto {nombre} está agotado.")
            else:
                messagebox.showerror("Error", f"El código '{codigo}' no pertenece a ningún producto registrado.")