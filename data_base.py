#aca tenemos que generar la base de datos de las cremas, cantidades y precios de cada una. con una simple descripcion de la misma. mas un codigo de id.#
import sqlite3
# Conectamos a la base de datos (o la creamos si no existe)
def crear_base_de_datos():
    conn = sqlite3.connect('cremas.db')
# Creamos un cursor para ejecutar comandos SQL
    cursor = conn.cursor()


# Creamos la tabla de cremas
    cursor.execute('''CREATE TABLE IF NOT EXISTS cremas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,       
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
    )''')

# Guardamos los cambios y cerramos la conexión
    conn.commit()       
    conn.close()
    
# Función para obtener todas las cremas de la base de datos    

from models import Crema

def obtener_cremas():
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cremas")
    resultados = cursor.fetchall()

    conn.close()

    # 🔥 conversión a objetos
    cremas = []
    for c in resultados:
        crema = Crema(
            id=c[0],
            nombre=c[1],
            descripcion=c[2],
            cantidad=c[3],
            precio=c[4]
        )
        cremas.append(crema)

    return cremas

# Función para insertar una nueva crema en la base de datos
def insertar_crema(nombre, descripcion, cantidad, precio):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cremas (nombre, descripcion, cantidad, precio)
        VALUES (?, ?, ?, ?)
    """, (nombre, descripcion, cantidad, precio))

    conn.commit()
    conn.close()

# Función para actualizar el stock de una crema existente
def actualizar_stock(id, cantidad_extra):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cremas
        SET cantidad = cantidad + ?
        WHERE id = ?
    """, (cantidad_extra, id))

    conn.commit()
    conn.close()

# Función para eliminar una crema de la base de datos
def eliminar_crema(id):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cremas WHERE id = ?", (id,))

    conn.commit()
    conn.close()


# Función para restar stock de una crema (por ejemplo, después de una venta)
def restar_stock(id, cantidad):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    # Primero obtenemos el stock actual
    cursor.execute("SELECT cantidad FROM cremas WHERE id = ?", (id,))
    resultado = cursor.fetchone()

    if resultado:
        stock_actual = resultado[0]

        # Validación: no permitir stock negativo
        if stock_actual >= cantidad:
            cursor.execute("""
                UPDATE cremas
                SET cantidad = cantidad - ?
                WHERE id = ?
            """, (cantidad, id))

    conn.commit()
    conn.close()