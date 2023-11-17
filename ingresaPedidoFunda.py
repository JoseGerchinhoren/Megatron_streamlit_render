import streamlit as st
import pyodbc
import json

def ingresaPedidoFunda(id_usuario):
    st.title("Registrar Pedido de Funda")

    # Campos para ingresar los datos del pedido de funda
    fecha = st.date_input("Fecha del Pedido:")
    pedido = st.text_input("Pedido:")
    nombreCliente = st.text_input("Nombre del Cliente:")
    Contacto = st.text_input("Contacto:")
    estado = st.selectbox("Estado:", [ "Señado", "Pedido", "Avisado", "Entregado", "Cancelado"])

    # Botón para registrar el pedido de funda
    st.button("Registrar Pedido"):

if __name__ == "__main__":
    ingresaPedidoFunda()
