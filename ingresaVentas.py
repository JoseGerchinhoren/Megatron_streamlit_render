import streamlit as st
import pyodbc
import json
from datetime import datetime

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Función para insertar una venta en la base de datos
def insertar_venta(fecha, producto, precio, metodo_pago, id_usuario):
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

        # Insertar la venta en la base de datos
        query = "INSERT INTO Ventas (fecha, productoVendido, precio, metodoPago, idUsuario) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (fecha, producto, precio, metodo_pago, id_usuario))
        conn.commit()
        conn.close()
        st.success("Venta registrada exitosamente")

    except Exception as e:
        st.error(f"Error al registrar la venta: {e}")

def venta(id_usuario):
    st.title("Registrar Venta")

    # Campos para ingresar los datos de la venta
    if st.session_state.user_rol == "admin":
        fecha = st.date_input("Fecha de la venta:")
    producto = st.text_input("Producto vendido:")
    precio = st.text_input("Precio:")
    if precio:
        if precio.isdigit():
            precio = int(precio)
        else:
            st.warning("El precio debe ser un número entero.")
            precio = None
    else:
        precio = None
    metodo_pago = st.selectbox("Método de pago:", ["Efectivo", "Transferencia", "Tarjeta de Crédito", "Tarjeta de Débito", "Otro"])

    # Botón para registrar la venta
    if st.button("Registrar Venta"):
        if st.session_state.user_rol == "admin":
            if fecha and producto and precio > 0 and metodo_pago:
                insertar_venta(fecha, producto, precio, metodo_pago, id_usuario)
            else:
                st.warning("Por favor, complete todos los campos.")
        else:
            if producto and precio > 0 and metodo_pago:
                insertar_venta(datetime.now(), producto, precio, metodo_pago, id_usuario)
            else:
                st.warning("Por favor, complete todos los campos.")

if __name__ == "__main__":
    venta()