import streamlit as st
import pandas as pd
import json

# Simular datos de configuración desde el archivo config.json
config = {
    "driver": "SimulatedDriver",
    "server": "SimulatedServer",
    "database": "SimulatedDatabase",
    "user": "SimulatedUser",
    "password": "SimulatedPassword"
}

# Función para simular la obtención de datos de pedidos de fundas
def obtener_datos_simulados():
    # Simular datos de pedidos de fundas
    data = {
        "ID": [1, 2, 3],
        "Fecha": ["2023-01-01", "2023-02-01", "2023-03-01"],
        "Pedido": ["Pedido1", "Pedido2", "Pedido3"],
        "Nombre del Cliente": ["Cliente1", "Cliente2", "Cliente3"],
        "Contacto": ["Contacto1", "Contacto2", "Contacto3"],
        "Estado": ["Avisado", "Entregado", "Señado"],
        "ID Usuario": [101, 102, 103],
        "Nombre de Usuario": ["Usuario1", "Usuario2", "Usuario3"],
    }

    # Crear un DataFrame simulado
    df = pd.DataFrame(data)

    return df

# Función para simular la edición del estado de un pedido de funda
def editar_estado_pedido_funda_simulado(pedidos_df, id_pedido_funda, nuevo_estado):
    # Verificar si el ID del pedido de funda existe en los datos simulados
    if id_pedido_funda not in pedidos_df['ID'].values:
        st.warning(f"El ID del Pedido de Funda {id_pedido_funda} no existe.")
        return

    # Actualizar el estado del pedido de funda en los datos simulados
    pedidos_df.loc[pedidos_df['ID'] == id_pedido_funda, 'Estado'] = nuevo_estado

    st.success(f"Estado del Pedido de Funda {id_pedido_funda} editado correctamente a: {nuevo_estado}")

# Función principal para la interfaz de usuario
def visualiza_pedidos_fundas():
    st.title("Visualizar Pedidos de Fundas")

    # Obtener datos simulados
    pedidos_df = obtener_datos_simulados()

    # Cambiar los nombres de las columnas
    pedidos_df.columns = ["ID", "Fecha", "Pedido", "Nombre del Cliente", "Contacto", "Estado", "ID Usuario", "Nombre de Usuario"]

    # Mostrar la tabla de pedidos de fundas
    st.dataframe(pedidos_df)

    # Sección para la edición del estado de registros simulada
    st.subheader("Editar Estado")
    id_pedido_funda = st.number_input("Ingrese el ID del Pedido de Funda que desea editar:", value=0)
    nuevo_estado = st.selectbox("Nuevo valor del campo estado:", ["Señado", "Pedido", "Avisado", "Entregado", "Cancelado"])

    if st.button("Guardar"):
        editar_estado_pedido_funda_simulado(pedidos_df, id_pedido_funda, nuevo_estado)

# Función principal
def main():
    visualiza_pedidos_fundas()

if __name__ == "__main__":
    main()
