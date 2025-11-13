from flask import Flask, request, render_template, redirect, url_for
from conexion import conectar

app = Flask(__name__)

# ====== INDEX ======
@app.route('/')
def index():
    return render_template('index.html')

# ====== REGISTRAR ESTUDIANTES ======
@app.route('/registrar_estudiantes', methods=['GET', 'POST'])
def registrar_estudiantes():
    conexion = conectar()
    cursor = conexion.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        curso = request.form['curso'].strip()
        correo = request.form.get('correo', '').strip()
        if correo == '':
            correo = None
        cursor.execute("SELECT COUNT(*) FROM estudiantes WHERE nombre = %s AND curso = %s", (nombre, curso))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO estudiantes (nombre, curso, correo) VALUES (%s, %s, %s)", (nombre, curso, correo))
            conexion.commit()
    cursor.execute("SELECT id, nombre, curso, correo FROM estudiantes ORDER BY nombre")
    estudiantes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('registrar_estudiantes.html', estudiantes=estudiantes)

# ====== REGISTRAR ASISTENCIA ======
@app.route('/registrar_asistencia', methods=['GET', 'POST'])
def registrar_asistencia():
    conexion = conectar()
    cursor = conexion.cursor()
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        presente = request.form['presente']
        cursor.execute("SELECT COUNT(*) FROM asistencia WHERE estudiante_id = %s AND fecha = CURDATE()", (estudiante_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO asistencia (estudiante_id, fecha, presente) VALUES (%s, CURDATE(), %s)", (estudiante_id, presente))
            conexion.commit()
    cursor.execute("""
        SELECT e.nombre, a.fecha, a.presente
        FROM asistencia a
        JOIN estudiantes e ON a.estudiante_id = e.id
        ORDER BY a.fecha DESC
    """)
    asistencias = cursor.fetchall()
    cursor.execute("SELECT id, nombre, curso FROM estudiantes ORDER BY nombre")
    estudiantes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('registrar_asistencia.html', asistencias=asistencias, estudiantes=estudiantes)

# ====== REGISTRAR COBROS ======
@app.route('/registrar_cobros', methods=['GET', 'POST'])
def registrar_cobros():
    conexion = conectar()
    cursor = conexion.cursor()
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        concepto = request.form['concepto'].strip()
        monto = request.form['monto']
        # Quitamos la columna 'estado'
        cursor.execute("""
            INSERT INTO cobros (estudiante_id, concepto, monto, fecha_pago)
            VALUES (%s, %s, %s, CURDATE())
        """, (estudiante_id, concepto, monto))
        conexion.commit()
    cursor.execute("""
        SELECT e.nombre, c.concepto, c.monto, c.fecha_pago
        FROM cobros c
        JOIN estudiantes e ON c.estudiante_id = e.id
        ORDER BY c.fecha_pago DESC
    """)
    cobros = cursor.fetchall()
    cursor.execute("SELECT id, nombre, curso FROM estudiantes ORDER BY nombre")
    estudiantes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('registrar_cobros.html', cobros=cobros, estudiantes=estudiantes)

# ====== REPORTES ======
@app.route('/reportes', methods=['GET', 'POST'])
def reportes():
    conexion = conectar()
    cursor = conexion.cursor()
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        fecha_reporte = request.form['fecha_reporte']
        tipo_reporte = request.form['tipo_reporte'].strip()
        descripcion = request.form['descripcion'].strip()
        cursor.execute("""
            INSERT INTO reportes (estudiante_id, fecha_reporte, tipo_reporte, descripcion)
            VALUES (%s, %s, %s, %s)
        """, (estudiante_id, fecha_reporte, tipo_reporte, descripcion))
        conexion.commit()

    # Reportes
    cursor.execute("""
        SELECT r.id, e.nombre, r.fecha_reporte, r.tipo_reporte, r.descripcion
        FROM reportes r
        JOIN estudiantes e ON r.estudiante_id = e.id
        ORDER BY r.fecha_reporte DESC
    """)
    reportes = cursor.fetchall()

    # Deudores (simplemente todos los cobros, sin estado)
    cursor.execute("""
        SELECT e.nombre, c.concepto, c.monto, c.fecha_pago
        FROM cobros c
        JOIN estudiantes e ON c.estudiante_id = e.id
        ORDER BY c.fecha_pago DESC
    """)
    deudores = cursor.fetchall()

    # Ausentes
    cursor.execute("""
        SELECT e.nombre, a.fecha
        FROM asistencia a
        JOIN estudiantes e ON a.estudiante_id = e.id
        WHERE a.presente=0
        ORDER BY a.fecha DESC
    """)
    ausentes = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM estudiantes ORDER BY nombre")
    estudiantes = cursor.fetchall()

    cursor.close()
    conexion.close()
    return render_template('reportes.html', reportes=reportes, deudores=deudores, ausentes=ausentes, estudiantes=estudiantes)

# ====== EJECUCIÓN ======
if __name__ == '__main__':
    app.run(debug=True)
