import sqlite3

class InventoryLogic:
    def __init__(self):
        self.db_path = "database/inventario.db"

    def buscar_producto(self, codigo):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE codigo=?", (codigo,))
        producto = cursor.fetchone()
        conexion.close()
        return producto # Devuelve una tupla: (codigo, nombre, precio, cantidad)

    def descontar_stock(self, codigo, cantidad_a_restar):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE codigo = ?", (cantidad_a_restar, codigo))
        conexion.commit()
        conexion.close()

    def obtener_todos(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conexion.close()
        return productos