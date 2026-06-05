import sqlite3
import pandas as pd

DB_NAME = "alphatech_records.db"

def crear_tablas():
    """Crea la estructura inicial de la base de datos si no existe."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        ID_Pedido TEXT PRIMARY KEY,
        Cliente TEXT,
        Producto TEXT,
        Estado TEXT,
        Dias_Desde_Entrega INTEGER
    )
    """)
    conexion.commit()
    conexion.close()

def insertar_datos_demo():
    """Inserta registros de prueba si la tabla está vacía."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    if cursor.fetchone()[0] == 0:
        datos = [
            ("ALFA-101", "Carlos Muñoz", "Laptop Pro 15", "Enviado", 5),
            ("ALFA-102", "Laura Restrepo", "Smartphone X", "Entregado", 12),
            ("ALFA-103", "Andrés Gómez", "Monitor 4K 27", "Procesando", 0),
            ("ALFA-104", "Sofía Díaz", "Licencia Windows 11", "Entregado", 45)
        ]
        cursor.executemany("INSERT INTO pedidos VALUES (?, ?, ?, ?, ?)", datos)
        conexion.commit()
    conexion.close()

def obtener_pedidos_df():
    """Extrae los datos frescos de la BD y los devuelve como un DataFrame de Pandas."""
    conexion = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pedidos", conexion)
    conexion.close()
    return df

def consultar_pedido_por_id(id_pedido):
    """Busca un pedido específico en SQLite y devuelve su información en texto."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM pedidos WHERE ID_Pedido = ?", (id_pedido.strip().upper(),))
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        return f"Pedido: {resultado[0]}, Cliente: {resultado[1]}, Producto: {resultado[2]}, Estado: {resultado[3]}, Días desde la entrega: {resultado[4]}"
    return "No se encontró ningún pedido con ese ID en la base de datos."

# El bloque de ejecución principal SIEMPRE va al final absoluto del archivo
if __name__ == "__main__":
    crear_tablas()
    insertar_datos_demo()
    print("¡Base de datos inicializada con éxito!")