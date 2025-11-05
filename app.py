from flask import Flask, request, render_template, redirect, url_for
from conexion import conectar

app = Flask(__name__)

# Conexión a la base de datos
db = conectar()

# ====== INDEX ======
@app.route('/')
def index():
    return render_template('index.html')

# ====== REGISTRAR ESTUDIANTES ======
@app.route('/registrar_estudiantes', methods=['GET', 'POST'])
def registrar_estudiantes():
    cursor = db.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        curso = request.form['curso'].strip()
        # Evitar duplicados
        cursor.execute("SELECT COUNT(*) FROM estudiantes WHERE nombre = %s", (nombre,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO estudiantes (nombre, curso) VALUES (%s, %s)", (nombre, curso))
            db.commit()
    # Consultar todos los estudiantes
    cursor.execute("SELECT DISTINCT nombre, curso FROM estudiantes ORDER BY nombre")
    estudiantes = cursor.fetchall()
    cursor.close()
    return render_template('registrar_estudiantes.html', estudiantes=estudiantes)

# ====== REGISTRAR ASISTENCIA ======
@app.route('/registrar_asistencia', methods=['GET', 'POST'])
def registrar_asistencia():
    cursor = db.cursor()
    if request.method == 'POST':
        nombre = request.form['estudiante_id'].strip()
        presente = request.form['presente']
        # Evitar duplicados por día
        cursor.execute("SELECT COUNT(*) FROM asistencia WHERE estudiante_id = %s AND fecha = CURDATE()", (nombre,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO asistencia (estudiante_id, fecha, presente) VALUES (%s, CURDATE(), %s)", (nombre, presente))
            db.commit()
    # Mostrar lista de asistencia
    cursor.execute("SELECT DISTINCT estudiante_id, fecha, presente FROM asistencia ORDER BY fecha DESC")
    asistencias = cursor.fetchall()
    cursor.close()
    return render_template('registrar_asistencia.html', asistencias=asistencias)

# ====== REGISTRAR COBROS ======
@app.route('/registrar_cobro', methods=['GET', 'POST'])
def registrar_cobro():
    cursor = db.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        monto = request.form['monto']
        estado = request.form['estado']
        # Evitar duplicados por día
        cursor.execute("SELECT COUNT(*) FROM cobros WHERE nombre = %s AND fecha = CURDATE()", (nombre,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO cobros (estudiante_id, concepto, monto, fecha_pago) VALUES (%s, %s, %s, CURDATE())", (nombre, monto, estado))
            db.commit()
    cursor.execute("SELECT DISTINCT estudiante_id, concepto, monto, fecha_pago FROM cobros ORDER BY fecha_pago DESC")
    cobros = cursor.fetchall()
    cursor.close()
    return render_template('registrar_cobro.html', cobros=cobros)

# ====== REPORTES ======
@app.route('/reportes')
def reportes():
    cursor = db.cursor()
    # Alumnos que no pagaron
    cursor.execute("SELECT nombre, monto, estado, fecha FROM cobros WHERE estado='Pendiente' ORDER BY fecha DESC")
    deudores = cursor.fetchall()
    # Alumnos que no asistieron
    cursor.execute("SELECT nombre, fecha FROM asistencia WHERE presente='No' ORDER BY fecha DESC")
    ausentes = cursor.fetchall()
    cursor.close()
    return render_template('reportes.html', deudores=deudores, ausentes=ausentes)

# ====== EJECUCIÓN ======
if __name__ == '__main__':
    app.run(debug=True)

