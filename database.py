import sqlite3

# Conexión con la base de datos
def conectar():
    return sqlite3.connect('finanzas_caseras.db')

# Crear tablas para el sistema de finanzas
def crear_tablas():
    conn = conectar()
    c = conn.cursor()

    # Crear tabla de transacciones
    c.execute('''
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,  -- 'Ingreso' o 'Egreso'
            monto REAL,
            categoria TEXT,
            medio_pago TEXT,
            banco TEXT,  -- Cambiado de 'banco' a 'banco' para mantener consistencia
            cuotas INTEGER,
            fecha_ultima_cuota TEXT,
            fecha TEXT
        )
    ''')

    # Crear tabla para categorías
    c.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT
        )
    ''')

    # Crear tabla para medios de pago
    c.execute('''
        CREATE TABLE IF NOT EXISTS medios_pago (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT
        )
    ''')

    # Crear tabla para bancos
    c.execute('''
        CREATE TABLE IF NOT EXISTS bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Función para agregar una transacción
def agregar_transaccion(tipo, monto, categoria, medio_pago, banco, cuotas, fecha_ultima_cuota, fecha):
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        INSERT INTO transacciones (tipo, monto, categoria, medio_pago, banco, cuotas, fecha_ultima_cuota, fecha)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tipo, monto, categoria, medio_pago, banco, cuotas, fecha_ultima_cuota, fecha))
    conn.commit()
    conn.close()

# Función para obtener todas las categorías
def obtener_categorias():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT nombre FROM categorias')
    categorias = [row[0] for row in c.fetchall()]
    conn.close()
    return categorias

# Función para obtener todos los bancos
def obtener_bancos():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT nombre FROM bancos')
    bancos = [row[0] for row in c.fetchall()]
    conn.close()
    return bancos

# Función para obtener todas las transacciones
def obtener_transacciones():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM transacciones')
    transacciones = c.fetchall()
    conn.close()
    return transacciones

# Función para obtener transacciones por tipo
def obtener_transacciones_por_tipo(tipo):
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM transacciones WHERE tipo = ?', (tipo,))
    transacciones = c.fetchall()
    conn.close()
    return transacciones

# Función para agregar una nueva categoría
def agregar_categoria(nombre_categoria):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre_categoria,))
    conn.commit()
    conn.close()

# Función para agregar un nuevo banco
def agregar_banco(nombre_banco):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT INTO bancos (nombre) VALUES (?)", (nombre_banco,))
    conn.commit()
    conn.close()

# Llamamos a la función para crear las tablas al inicio
crear_tablas()














