from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database
from datetime import datetime  # Importar para manejar la fecha automática

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave segura en producción

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingresos', methods=['GET', 'POST'])
def ingresos():
    if request.method == 'POST':
        try:
            monto = float(request.form['monto'])  # Obtener el monto del formulario
            medio_pago = request.form['medio_pago']  # Obtener el medio de pago
            banco_entidad = request.form['banco_entidad'] if medio_pago == 'Transferencia' else None

            # Obtener la fecha actual automáticamente
            fecha = datetime.now().strftime('%Y-%m-%d')

            # Llamar a la función de agregar transacción
            database.agregar_transaccion('Ingreso', monto, None, medio_pago, banco_entidad, None, None, fecha)
            flash('Ingreso agregado exitosamente', 'success')  # Mensaje de éxito
            return redirect(url_for('ingresos'))  # Redirigir a la misma página después de agregar

        except Exception as e:
            print(f"Error al agregar ingreso: {e}")  # Imprimir el error en la consola

    # Obtener bancos para el formulario (categorías removidas)
    bancos = database.obtener_bancos()
    return render_template('ingresos.html', bancos=bancos)

@app.route('/egresos', methods=['GET', 'POST'])
def egresos():
    if request.method == 'POST':
        try:
            monto = float(request.form['monto'])  # Obtener el monto del formulario
            categoria = request.form['categoria']  # Obtener la categoría
            medio_pago = request.form['medio_pago']  # Obtener el medio de pago
            banco_entidad = request.form['banco_entidad'] if medio_pago in ['Tarjeta de Credito', 'Tarjeta de Debito', 'MODO'] else None
            cuotas = int(request.form['cuotas']) if 'cuotas' in request.form else None
            fecha_ultima_cuota = request.form['fecha_ultima_cuota'] if cuotas else None
            fecha = request.form['fecha']  # Obtener la fecha

            # Llamar a la función de agregar transacción
            database.agregar_transaccion('Egreso', monto, categoria, medio_pago, banco_entidad, cuotas, fecha_ultima_cuota, fecha)
            flash('Egreso agregado exitosamente', 'success')  # Mensaje de éxito
            return redirect(url_for('egresos'))  # Redirigir a la misma página después de agregar

        except Exception as e:
            print(f"Error al agregar egreso: {e}")  # Imprimir el error en la consola

    # Obtener categorías y bancos para el formulario
    categorias = database.obtener_categorias()
    bancos = database.obtener_bancos()
    return render_template('egresos.html', categorias=categorias, bancos=bancos)

@app.route('/transacciones')
def transacciones():
    transacciones = database.obtener_transacciones()  # Obtener todas las transacciones

    # Calcular el saldo total
    saldo = sum(transaccion[2] for transaccion in transacciones if transaccion[1] == 'Ingreso') - \
            sum(transaccion[2] for transaccion in transacciones if transaccion[1] == 'Egreso')

    # Crear los datos de egresos por categoría para el gráfico
    egresos = [transaccion for transaccion in transacciones if transaccion[1] == 'Egreso']
    egresos_por_categoria = {}
    for egreso in egresos:
        categoria = egreso[3]
        monto = egreso[2]
        if categoria in egresos_por_categoria:
            egresos_por_categoria[categoria] += monto
        else:
            egresos_por_categoria[categoria] = monto

    # Pasar los datos a la plantilla
    return render_template('transacciones.html', transacciones=transacciones, saldo=saldo, egresos_por_categoria=egresos_por_categoria)

@app.route('/agregar_categoria', methods=['GET', 'POST'])
def agregar_categoria():
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']
        database.agregar_categoria(nombre_categoria)
        flash('Categoría agregada exitosamente', 'success')  # Mensaje de éxito
        return redirect(url_for('agregar_categoria'))  # Redirigir a la misma página para mostrar el mensaje

    return render_template('agregar_categoria.html')

@app.route('/agregar_banco', methods=['GET', 'POST'])
def agregar_banco():
    if request.method == 'POST':
        nombre_banco = request.form['nombre_banco']
        database.agregar_banco(nombre_banco)
        flash('Banco agregado exitosamente', 'success')  # Mensaje de éxito
        return redirect(url_for('agregar_banco'))  # Redirigir a la misma página para mostrar el mensaje

    return render_template('agregar_banco.html')

if __name__ == '__main__':
    app.run(debug=True)



















