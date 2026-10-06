import sqlite3
import os

class DBManager:
    def __init__(self):
        # Asegura que la carpeta de la base de datos exista
        os.makedirs("database", exist_ok=True)
        self.db_path = "database/inventario.db"
        self.crear_tablas()

    def crear_tablas(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        
        # Crea la tabla si es la primera vez que se abre el programa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL
            )
        ''')
        conexion.commit()
        conexion.close()

    def agregar_producto(self, codigo, nombre, precio, cantidad):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, precio, cantidad)
                VALUES (?, ?, ?, ?)
            ''', (codigo, nombre, precio, cantidad))
            conexion.commit()
            return True, "Producto agregado correctamente."
        except sqlite3.IntegrityError:
            # Falla si intentas agregar un código que ya existe
            return False, f"Error: El código '{codigo}' ya existe en el inventario."
        finally:
            conexion.close()