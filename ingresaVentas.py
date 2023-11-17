import streamlit as st
import pyodbc
import json
from datetime import datetime

def venta():
    st.title("Registrar Venta")

    # Campos para ingresar los datos de la venta
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
    st.button("Registrar Venta")

if __name__ == "__main__":
    venta()