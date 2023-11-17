import streamlit as st
import pandas as pd
import json
import datetime

# Simular datos de configuración desde el archivo config.json
config = {
    "driver": "SimulatedDriver",
    "server": "SimulatedServer",
    "database": "SimulatedDatabase",
    "user": "SimulatedUser",
    "password": "SimulatedPassword"
}

# Simular datos de ventas
ventas_data = {
    "ID": [1, 2, 3],
    "Fecha": ["2023-01-01", "2023-02-01", "2023-03-01"],
    "Producto Vendido": ["Producto1", "Producto2", "Producto3"],
    "Precio": [100, 150, 200],
    "Metodo de Pago": ["Efectivo", "Tarjeta de Crédito", "Transferencia"],
    "ID Usuario": [101, 102, 103]
}

# Crear un DataFrame simulado de ventas
ventas_df = pd.DataFrame(ventas_data)

# Configurar el estado de la sesión para simular el rol del usuario
st.session_state.user_rol = "admin"

def visualiza_ventas():
    st.title("Visualizar Ventas")

    # Construir la consulta simulada
    st.sidebar.checkbox("Ventas del día")
    st.sidebar.checkbox("Ventas del mes")

    # Filtrar por ID de Usuario simulado
    id_usuario = st.sidebar.text_input("Filtrar por ID de Usuario", key="id_usuario")

    # Filtrar los datos simulados según los filtros seleccionados
    if id_usuario:
        ventas_df = ventas_df[ventas_df["ID Usuario"] == int(id_usuario)]

    # Mostrar la tabla simulada de ventas
    st.dataframe(ventas_df)

    # Calcular y mostrar el total de precios simulado
    total_precios = ventas_df["Precio"].sum()
    st.title(f"Total de Ventas: ${total_precios:}")

    # Calcular y mostrar el total por método de pago simulado
    for metodo_pago in ventas_df["Metodo de Pago"].unique():
        total_metodo_pago = ventas_df[ventas_df["Metodo de Pago"] == metodo_pago]["Precio"].sum()
        st.write(f"Total en {metodo_pago}: ${total_metodo_pago:}")

def editar_ventas():
    st.title("Editar Ventas")

    # Agregar un campo para ingresar el idVenta
    id_venta_editar = st.text_input("Ingrese el ID de la Venta que desea editar:")

    if id_venta_editar:
        # Consultar la venta específica por ID simulado
        venta_editar_df = ventas_df[ventas_df['ID'] == int(id_venta_editar)]

        # Verificar el rol del usuario simulado
        if st.session_state.user_rol == "admin":
            if not venta_editar_df.empty:
                # Mostrar la información actual de la venta simulada
                st.write("Información actual de la venta:")
                st.dataframe(venta_editar_df)

                # Mostrar campos para editar cada variable simulada
                for column in venta_editar_df.columns:
                    nuevo_valor = st.text_input(f"Nuevo valor para {column}", value=venta_editar_df.iloc[0][column])
                    venta_editar_df.at[venta_editar_df.index[0], column] = nuevo_valor

                # Botón para guardar los cambios simulados
                if st.button("Guardar cambios"):
                    st.success("¡Venta actualizada correctamente!")

            else:
                st.warning(f"No se encontró ninguna venta con el ID {id_venta_editar}")

        if not st.session_state.user_rol == "admin":
            if not venta_editar_df.empty:
                # Mostrar la información actual de la venta simulada
                st.write("Campos que puede modificar:")
                st.dataframe(venta_editar_df)

                # Mostrar campos para editar cada variable simulada
                for column in ["Producto Vendido", "Precio", "Metodo de Pago"]:
                    nuevo_valor = st.text_input(f"Nuevo valor para {column}", value=venta_editar_df.iloc[0][column])
                    venta_editar_df.at[venta_editar_df.index[0], column] = nuevo_valor

                # Botón para guardar los cambios simulados
                if st.button("Guardar cambios"):
                    st.success("¡Venta actualizada correctamente!")

            else:
                st.warning(f"No se encontró ninguna venta con el ID {id_venta_editar}")

def main():
    visualiza_ventas()  # Mostrar sección de visualización para todos los usuarios

    editar_ventas()  # Mostrar sección de edición solo para admin

if __name__ == "__main__":
    main()
