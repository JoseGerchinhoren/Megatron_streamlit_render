import streamlit as st
import pyodbc
import json
import re
from datetime import datetime


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
    st.button("Crear Usuario")

if __name__ == "__main__":
    crear_usuario()