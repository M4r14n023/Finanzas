import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Conexión con la base de datos
def conectar():
    return sqlite3.connect('finanzas_caseras.db')

# Crear tablas para el sistema de finanzas y usuarios
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
            banco TEXT,
            cuotas INTEGER,
            fecha_ultima_cuota TEXT,
            fecha TEXT,
            usuario_id INTEGER,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # Crear tabla para categorías
    c.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
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

    # Crear tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Función para agregar una transacción
def agregar_transaccion(tipo, monto, categoria, medio_pago, banco, cuotas, fecha_ultima_cuota, fecha, usuario_id):
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        INSERT INTO transacciones (tipo, monto, categoria, medio_pago, banco, cuotas, fecha_ultima_cuota, fecha, usuario_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tipo, monto, categoria, medio_pago, banco, cuotas, fecha_ultima_cuota, fecha, usuario_id))
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

# Función para obtener todas las transacciones de un usuario específico
def obtener_transacciones(usuario_id):
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM transacciones WHERE usuario_id = ?', (usuario_id,))
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

# Funciones relacionadas con el manejo de usuarios

# Función para registrar un usuario
def agregar_usuario(username, password_hash):
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Usuario ya existe
    conn.close()
    return True

# Función para obtener un usuario por su nombre de usuario
def obtener_usuario(username):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

# Función para obtener un usuario por su id
def obtener_usuario_por_id(user_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

# Nueva función: Borrar todas las transacciones de un usuario
def borrar_todas_transacciones(usuario_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM transacciones WHERE usuario_id = ?", (usuario_id,))
    conn.commit()
    conn.close()

# Nueva función: Obtener un egreso por su ID
def obtener_transaccion_por_id(transaccion_id, tipo):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM transacciones WHERE id = ? AND tipo = ?", (transaccion_id, tipo))
    transaccion = c.fetchone()
    conn.close()
    return transaccion

# Nueva función: Actualizar un egreso
def actualizar_egreso(transaccion_id, monto, categoria, medio_pago, banco, cuotas, fecha_ultima_cuota, fecha):
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        UPDATE transacciones
        SET monto = ?, categoria = ?, medio_pago = ?, banco = ?, cuotas = ?, fecha_ultima_cuota = ?, fecha = ?
        WHERE id = ? AND tipo = 'Egreso'
    ''', (monto, categoria, medio_pago, banco, cuotas, fecha_ultima_cuota, fecha, transaccion_id))
    conn.commit()
    conn.close()

# Llamamos a la función para crear las tablas al inicio
crear_tablas()


