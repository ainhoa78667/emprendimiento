from flask import Flask, request, render_template
from conexion import conectar

app = Flask(__name__)

# Crear la conexión
db = conectar()

@app.route('/')
def index():
    return render_template('index.html')  # asegúrate de tener este HTML en la carpeta "templates"

@app.route('/registrar_asistencia', methods=['POST'])
def registrar_asistencia():
    nombre = request.form['nombre']
    presente = request.form['presente']

    cursor = db.cursor()
    sql = "INSERT INTO asistencia (nombre, fecha, presente) VALUES (%s, CURDATE(), %s)"
    valores = (nombre, presente)
    cursor.execute(sql, valores)
    db.commit()
    cursor.close()

    return "✅ Asistencia registrada correctamente"

if __name__ == '__main__':
    app.run(debug=True)
