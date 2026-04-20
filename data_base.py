import sqlite3
from models import Crema

def crear_base_de_datos():
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cremas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            precio_costo REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def obtener_cremas():
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cremas")
    resultados = cursor.fetchall()

    conn.close()

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


def insertar_crema(nombre, descripcion, cantidad, precio, precio_costo):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cremas (nombre, descripcion, cantidad, precio, precio_costo)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, cantidad, precio, precio_costo))

    conn.commit()
    conn.close()

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


def eliminar_crema(id):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cremas WHERE id = ?", (id,))

    conn.commit()
    conn.close()


def restar_stock(id, cantidad):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT cantidad FROM cremas WHERE id = ?", (id,))
        resultado = cursor.fetchone()

        if resultado:
            stock_actual = resultado[0]

            if stock_actual >= cantidad:
                cursor.execute("""
                    UPDATE cremas
                    SET cantidad = cantidad - ?
                    WHERE id = ?
                """, (cantidad, id))
            else:
                raise ValueError("Stock insuficiente")

        conn.commit()

    finally:
        conn.close()

def buscar_cremas(nombre):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM cremas
        WHERE nombre LIKE ?
    """, (f"%{nombre}%",))

    resultados = cursor.fetchall()
    conn.close()

    cremas = []
    for c in resultados:
        cremas.append(Crema(*c))

    return cremas

def actualizar_crema(id, descripcion, precio):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cremas
        SET descripcion = ?, precio = ?
        WHERE id = ?
    """, (descripcion, precio, id))

    conn.commit()
    conn.close()

def crear_tabla_ventas():
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
   CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crema_id INTEGER,
    cantidad INTEGER,
    precio_venta REAL,
    precio_costo REAL,
    ganancia REAL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
    conn.commit()
    conn.close()

def registrar_venta(producto_id, cantidad):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cantidad, precio, precio_costo
        FROM cremas
        WHERE id = ?
    """, (producto_id,))

    producto = cursor.fetchone()

    if not producto:
        return "Producto no encontrado"

    stock, precio_venta, precio_costo = producto

    if stock < cantidad:
        return "Stock insuficiente"

    # 🔥 ganancia real
    ganancia = (precio_venta - precio_costo) * cantidad

    # 1. descontar stock
    cursor.execute("""
        UPDATE cremas
        SET cantidad = ?
        WHERE id = ?
    """, (stock - cantidad, producto_id))

    # 2. guardar venta (con ganancia)
    cursor.execute("""
        INSERT INTO ventas (
            crema_id,
            cantidad,
            precio_venta,
            precio_costo,
            ganancia
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        producto_id,
        cantidad,
        precio_venta,
        precio_costo,
        ganancia
    ))

    conn.commit()
    conn.close()

    return "Venta registrada correctamente"



def calcular_ganancia_total():
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM((precio_venta - precio_costo) * cantidad)
        FROM ventas
    """)

    resultado = cursor.fetchone()[0]

    conn.close()

    return resultado if resultado else 0

def total_ganancia():
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(ganancia) FROM ventas")
    resultado = cursor.fetchone()[0]

    conn.close()
    return resultado if resultado else 0

def total_vendido():
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(cantidad * precio_venta)
        FROM ventas
    """)

    resultado = cursor.fetchone()[0]
    conn.close()

    return resultado if resultado else 0

def obtener_ventas():
    conn = sqlite3.connect("cremas.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, crema_id, cantidad, precio_venta, precio_costo, fecha
        FROM ventas
        ORDER BY fecha DESC
    """)

    ventas = cursor.fetchall()
    conn.close()
    return ventas

def procesar_ventas_con_ganancia(ventas):
    resultado = []

    for v in ventas:
        id, crema_id, cantidad, precio_venta, precio_costo, fecha = v

        ganancia = (precio_venta - precio_costo) * cantidad

        resultado.append({
            "id": id,
            "crema_id": crema_id,
            "cantidad": cantidad,
            "precio_venta": precio_venta,
            "precio_costo": precio_costo,
            "ganancia": ganancia,
            "fecha": fecha
        })

    return resultado