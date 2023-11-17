import streamlit as st
import pyodbc
import json
from ingresaVentas import venta
from creaUsuarios import crear_usuario
from visualizaVentas import main as visualiza_ventas
from ingresaPedidoFunda import ingresaPedidoFunda
from visualizaPedidosFundas import visualiza_pedidos_fundas
from ingresaArreglo import ingresa_arreglo_tecnico
from visualizaArreglos import visualizar_arreglos
from visualizaUsuarios import main as visualizar_usuarios

def main():
    st.title("Megatron Accesorios")
    st.sidebar.title("Menú")

    selected_option = st.sidebar.selectbox("Seleccione una opción:", ["Inicio", "Nueva Venta", "Visualizar Ventas", "Nuevo Pedido de Funda", "Visualizar Pedidos de Fundas", "Nuevo Servicio Tecnico", "Visualizar Servicios Tecnicos", "Crear Usuario", "Visualizar Usuarios"])
    if selected_option == "Nueva Venta":
        venta()
    if selected_option == "Crear Usuario":
        crear_usuario()
    if selected_option == "Visualizar Ventas":
        visualiza_ventas()
    if selected_option == "Nuevo Pedido de Funda":
        ingresaPedidoFunda()
    if selected_option == "Visualizar Pedidos de Fundas":
        visualiza_pedidos_fundas()
    if selected_option == "Nuevo Servicio Tecnico":
        ingresa_arreglo_tecnico()
    if selected_option == "Visualizar Servicios Tecnicos":
        visualizar_arreglos()
    if selected_option == "Visualizar Usuarios":
        visualizar_usuarios()

    if selected_option == "Inicio":
        st.write(f"Bienvenido! - Megatron Accesorios - Sistema de Gestión")

if __name__ == "__main__":
    main()