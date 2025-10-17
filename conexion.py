import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="sistema_cobros"
    )
    if conexion.is_connected():
        print("✅ Conexión exitosa a MySQL")
    return conexion
