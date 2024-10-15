from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import database
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirigir a esta ruta si no se ha iniciado sesión

# Manejo de sesiones
login_manager.session_protection = 'strong'

# Procesador de contexto para inyectar el usuario en todas las plantillas
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    user = database.obtener_usuario_por_id(user_id)
    if user:
        return User(user[0], user[1], user[2])  # id, username, password
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        try:
            database.agregar_usuario(username, hashed_password)
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.obtener_usuario(username)

        if user and check_password_hash(user[2], password):  # Verificar la contraseña
            login_user(User(user[0], user[1], user[2]))
            return redirect(url_for('index'))  # Redirigir al dashboard
        flash('Nombre de usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/ingresos', methods=['GET', 'POST'])
@login_required
def ingresos():
    if request.method == 'POST':
        try:
            monto = float(request.form['monto'])
            medio_pago = request.form['medio_pago']
            banco_entidad = request.form['banco_entidad'] if medio_pago == 'Transferencia' else None
            fecha = datetime.now().strftime('%Y-%m-%d')
            database.agregar_transaccion('Ingreso', monto, None, medio_pago, banco_entidad, None, None, fecha, current_user.id)
            flash('Ingreso agregado exitosamente', 'success')
            return redirect(url_for('ingresos'))
        except Exception as e:
            flash(f"Error al agregar ingreso: {e}", 'danger')
    bancos = database.obtener_bancos()
    return render_template('ingresos.html', bancos=bancos)

@app.route('/egresos', methods=['GET', 'POST'])
@login_required
def egresos():
    if request.method == 'POST':
        try:
            monto = float(request.form['monto'])
            categoria = request.form['categoria']
            medio_pago = request.form['medio_pago']
            banco_entidad = request.form['banco_entidad'] if medio_pago in ['Tarjeta de Credito', 'Tarjeta de Debito', 'MODO'] else None
            cuotas = int(request.form['cuotas']) if 'cuotas' in request.form else None
            fecha_ultima_cuota = request.form['fecha_ultima_cuota'] if cuotas else None
            fecha = request.form['fecha']
            database.agregar_transaccion('Egreso', monto, categoria, medio_pago, banco_entidad, cuotas, fecha_ultima_cuota, fecha, current_user.id)
            flash('Egreso agregado exitosamente', 'success')
            return redirect(url_for('egresos'))
        except Exception as e:
            flash(f"Error al agregar egreso: {e}", 'danger')

    categorias = database.obtener_categorias()
    bancos = database.obtener_bancos()
    return render_template('egresos.html', categorias=categorias, bancos=bancos)

@app.route('/transacciones')
@login_required
def transacciones():
    transacciones = database.obtener_transacciones(current_user.id)
    saldo = sum(t[2] for t in transacciones if t[1] == 'Ingreso') - \
            sum(t[2] for t in transacciones if t[1] == 'Egreso')
    egresos = [t for t in transacciones if t[1] == 'Egreso']
    egresos_por_categoria = {}
    for egreso in egresos:
        categoria = egreso[3]
        monto = egreso[2]
        egresos_por_categoria[categoria] = egresos_por_categoria.get(categoria, 0) + monto
    return render_template('transacciones.html', transacciones=transacciones, saldo=saldo, egresos_por_categoria=egresos_por_categoria)

@app.route('/agregar_categoria', methods=['GET', 'POST'])
@login_required
def agregar_categoria():
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']
        try:
            database.agregar_categoria(nombre_categoria)
            flash('Categoría agregada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al agregar categoría: {e}', 'danger')
        return redirect(url_for('agregar_categoria'))
    return render_template('agregar_categoria.html')

@app.route('/agregar_banco', methods=['GET', 'POST'])
@login_required
def agregar_banco():
    if request.method == 'POST':
        nombre_banco = request.form['nombre_banco']
        try:
            database.agregar_banco(nombre_banco)
            flash('Banco agregado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al agregar banco: {e}', 'danger')
        return redirect(url_for('agregar_banco'))
    return render_template('agregar_banco.html')

if __name__ == '__main__':
    app.run(debug=True)






















