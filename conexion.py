import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="bmf20zlghgsykdwrepqz-mysql.services.clever-cloud.com",
        user="u7ygwvuuyrm14duz",
        password="DMG2kzTOgiWHQei2QJtx",
        database="bmf20zlghgsykdwrepqz"
    )
    if conexion.is_connected():
        print("✅ Conexión exitosa a MySQL")
    return conexion
