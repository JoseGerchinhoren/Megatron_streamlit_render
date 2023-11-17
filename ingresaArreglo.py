import streamlit as st
import pyodbc
import json


def ingresa_arreglo_tecnico(idUsuario):
    st.title("Registrar Pedido de Arreglo Técnico")

    # Campos para ingresar los datos del arreglo técnico
    fecha = st.date_input("Fecha del Arreglo:")
    nombreCliente = st.text_input("Nombre del Cliente:")
    contacto = st.text_input("Número o Email de Contacto:")
    modelo = st.text_input("Producto a Arreglar:")
    falla = st.text_input("Falla:")
    tipoDesbloqueo = st.text_input("Contraseña o Patrón de Desbloqueo:")
    
    # Cargar imagen para el patrón de desbloqueo
    imagen_patron = st.file_uploader("Cargar Imagen para Patrón de Desbloqueo", type=["jpg", "jpeg", "png"])

    estado_options = ["A arreglar", "En el técnico", "Avisado al Cliente", "Entregado"]
    estado = st.selectbox("Estado:", estado_options)

    observaciones = st.text_input("Observaciones:")

    # Botón para registrar el arreglo técnico
    st.button("Registrar Arreglo Técnico"):

if __name__ == "__main__":
    ingresa_arreglo_tecnico()
