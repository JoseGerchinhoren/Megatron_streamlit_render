import streamlit as st
import pyodbc
import json
import re
from datetime import datetime

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Función para insertar un nuevo usuario en la base de datos
def insertar_usuario(nombreApellido, email, contrasena, fechaNacimiento, dni, domicilio, rol):
    try:
        # Conexión a la base de datos SQL Server
        conn_str = (
            f"DRIVER={{{config['driver']}}};"
            f"SERVER={config['server']};"
            f"DATABASE={config['database']};"
            f"UID={config['user']};"
            f"PWD={config['password']};"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Transformar la fecha al formato "AAAA-MM-DD"
        fechaNacimiento = datetime.strptime(fechaNacimiento, "%d/%m/%Y").strftime("%Y-%m-%d")

        # Insertar el nuevo usuario en la base de datos
        query = "EXEC CrearUsuario ?, ?, ?, ?, ?, ?, ?"
        cursor.execute(query, (nombreApellido, email, contrasena, fechaNacimiento, dni, domicilio, rol))
        conn.commit()
        conn.close()
        st.success("Usuario creado exitosamente")

    except Exception as e:
        st.error(f"Error al crear el usuario: {e}")

def crear_usuario():
    st.title("Crear Usuario")

    # Campos para ingresar los datos del nuevo usuario
    nombreApellido = st.text_input("Nombre y Apellido:")
    email = st.text_input("Correo Electrónico:")
    contrasena = st.text_input("Contraseña:", type="password")
    verificacionContrasena = st.text_input("Confirmar Contraseña:", type="password")
    
    # Campo de fecha de nacimiento
    fechaNacimiento = st.text_input("Fecha de Nacimiento:")
    if not re.match(r'\d{2}/\d{2}/\d{4}', fechaNacimiento):
        st.warning("El formato de fecha debe ser DD/MM/AAAA.")
    
    dni = st.text_input("DNI:")
    domicilio = st.text_input("Domicilio:")
    
    # Campo de rol
    rol = st.selectbox("Rol:", ["admin", "empleado"])

    # Botón para crear el nuevo usuario
    if st.button("Crear Usuario"):
        if nombreApellido and email and contrasena and verificacionContrasena and contrasena == verificacionContrasena and re.match(r'\d{2}/\d{2}/\d{4}', fechaNacimiento) and dni and rol:
            insertar_usuario(nombreApellido, email, contrasena, fechaNacimiento, dni, domicilio, rol)
        else:
            if contrasena != verificacionContrasena:
                st.warning("Las contraseñas no coinciden. Por favor, verifique.")
            else:
                st.warning("Por favor, complete todos los campos correctamente.")

if __name__ == "__main__":
    crear_usuario()