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
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
    conn.commit()
    conn.close()

def registrar_venta(crema_id, cantidad):
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT cantidad, precio, precio_costo
            FROM cremas
            WHERE id = ?
        """, (crema_id,))
        
        resultado = cursor.fetchone()

        if resultado:
            stock_actual, precio_venta, precio_costo = resultado

            if stock_actual >= cantidad:
                # Restar stock
                cursor.execute("""
                    UPDATE cremas
                    SET cantidad = cantidad - ?
                    WHERE id = ?
                """, (cantidad, crema_id))

                # 🔥 SNAPSHOT
                cursor.execute("""
                    INSERT INTO ventas (crema_id, cantidad, precio_venta, precio_costo)
                    VALUES (?, ?, ?, ?)
                """, (crema_id, cantidad, precio_venta, precio_costo))
            else:
                raise ValueError("Stock insuficiente")

        conn.commit()

    finally:
        conn.close()


def obtener_ventas():
    conn = sqlite3.connect('cremas.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ventas.id, cremas.nombre, ventas.cantidad, ventas.fecha
        FROM ventas
        JOIN cremas ON ventas.crema_id = cremas.id
        ORDER BY ventas.fecha DESC
    """)

    resultados = cursor.fetchall()
    conn.close()

    return resultados

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