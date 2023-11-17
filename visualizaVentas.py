import streamlit as st
import pyodbc
import pandas as pd
import json
import datetime

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Conexión a la base de datos SQL Server
db = pyodbc.connect(
    driver=config["driver"],
    server=config["server"],
    database=config["database"],
    uid=config["user"],
    pwd=config["password"]
)

def visualiza_ventas():
    st.title("Visualizar Ventas")

    # Construir la consulta SQL en función de los filtros
    query = "SELECT * FROM Ventas WHERE 1 = 1"

    # Filtro de fecha
    fecha_filtro = None
    if st.sidebar.checkbox("Ventas del día"):
        fecha_filtro = (datetime.date.today(), datetime.date.today())
    elif st.sidebar.checkbox("Ventas del mes"):
        today = datetime.date.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=1, month=today.month + 1) - datetime.timedelta(days=1)
        fecha_filtro = (first_day_of_month, last_day_of_month)

    # Filtro de ID de Usuario
    id_usuario = st.sidebar.text_input("Filtrar por ID de Usuario", key="id_usuario")

    # Construir la consulta SQL en función de los filtros
    if fecha_filtro:
        query += f" AND fecha >= '{fecha_filtro[0]}' AND fecha <= '{fecha_filtro[1]}'"

    if id_usuario:
        query += f" AND idUsuario = '{id_usuario}'"
    
    query += " ORDER BY idVenta DESC"

    # Ejecutar la consulta y obtener los resultados en un DataFrame
    ventas_df = pd.read_sql(query, db)

    # Consulta SQL para obtener la información de los usuarios
    query_usuarios = "SELECT idUsuario, nombreApellido FROM Usuarios"
    usuarios_df = pd.read_sql(query_usuarios, db)

    # Fusionar (unir) el DataFrame de ventas con el DataFrame de usuarios
    ventas_df = pd.merge(ventas_df, usuarios_df, on="idUsuario", how="left")

    # Cambiar los nombres de las columnas
    ventas_df.columns = ["ID", "Fecha", "Producto Vendido", "Precio", "Metodo de Pago", "ID Usuario", "Nombre de Usuario"]

    # Cambiar el orden del DataFrame
    ventas_df = ventas_df[[
        "ID", "Fecha", "Producto Vendido", "Precio", "Metodo de Pago", "ID Usuario", "Nombre de Usuario"
    ]]

    # Mostrar la tabla de ventas con la nueva columna de nombre de usuario
    st.dataframe(ventas_df)

    # Calcular y mostrar el total de precios
    total_precios = ventas_df["Precio"].sum()
    st.title(f"Total de Ventas: ${total_precios:}")

    # Calcular y mostrar el total por método de pago
    total_efectivo = ventas_df[ventas_df["Metodo de Pago"] == "Efectivo"]["Precio"].sum()
    total_transferencia = ventas_df[ventas_df["Metodo de Pago"] == "Transferencia"]["Precio"].sum()
    total_credito = ventas_df[ventas_df["Metodo de Pago"] == "Tarjeta de Crédito"]["Precio"].sum()
    total_debito = ventas_df[ventas_df["Metodo de Pago"] == "Tarjeta de Débito"]["Precio"].sum()
    total_otro = ventas_df[ventas_df["Metodo de Pago"] == "Otro"]["Precio"].sum()
    

    st.write(f"Total en Efectivo: ${total_efectivo:}")
    st.write(f"Total en Transferencia: ${total_transferencia:}")
    st.write(f"Total en Tarjeta de Crédito: ${total_credito:}")
    st.write(f"Total en Tarjeta de Débito: ${total_debito:}")
    st.write(f"Total en Otro: ${total_otro:}")

def editar_ventas():
    st.title("Editar Ventas")

    # Agregar un campo para ingresar el idVenta
    id_venta_editar = st.text_input("Ingrese el ID de la Venta que desea editar:")

    if id_venta_editar:
        # Consultar la venta específica por ID
        query_venta = f"SELECT * FROM Ventas WHERE idVenta = {id_venta_editar}"
        venta_editar_df = pd.read_sql(query_venta, db)

        # Verificar si el usuario es admin
        if st.session_state.user_rol == "admin":

            if not venta_editar_df.empty:
                # Mostrar la información actual de la venta
                st.write("Información actual de la venta:")
                # Cambiar los nombres de las columnas
                venta_editar_df.columns = ["ID", "Fecha", "Producto Vendido", "Precio", "Metodo de Pago", "ID Usuario"]

                # Cambiar el orden del DataFrame
                venta_editar_df = venta_editar_df[[
                    "ID", "Fecha", "Producto Vendido", "Precio", "Metodo de Pago", "ID Usuario"
                ]]

                st.dataframe(venta_editar_df)

                # Mostrar campos para editar cada variable
                for column in venta_editar_df.columns:
                    nuevo_valor = st.text_input(f"Nuevo valor para {column}", value=venta_editar_df.iloc[0][column])
                    venta_editar_df.at[0, column] = nuevo_valor

                # Botón para guardar los cambios
                if st.button("Guardar cambios"):
                    # Actualizar la venta en la base de datos
                    nueva_informacion = {
                        "fecha": venta_editar_df.at[0, "Fecha"],
                        "productoVendido": venta_editar_df.at[0, "Producto Vendido"],
                        "precio": venta_editar_df.at[0, "Precio"],
                        "metodoPago": venta_editar_df.at[0, "Metodo de Pago"],
                        "idUsuario": venta_editar_df.at[0, "ID Usuario"]
                    }

                    # Generar la sentencia SQL UPDATE
                    update_query = f"""
                        UPDATE Ventas
                        SET
                            fecha = '{nueva_informacion["fecha"]}',
                            productoVendido = '{nueva_informacion["productoVendido"]}',
                            precio = {nueva_informacion["precio"]},
                            metodoPago = '{nueva_informacion["metodoPago"]}',
                            idUsuario = {nueva_informacion["idUsuario"]}
                        WHERE idVenta = {id_venta_editar}
                    """

                    # Ejecutar la sentencia SQL UPDATE
                    cursor = db.cursor()
                    cursor.execute(update_query)
                    db.commit()

                    st.success("¡Venta actualizada correctamente!")

            else:
                st.warning(f"No se encontró ninguna venta con el ID {id_venta_editar}")
        
        if not st.session_state.user_rol == "admin":
            if not venta_editar_df.empty:
                # Mostrar la información actual de la venta
                st.write("Campos que puede modificar:")
                # Cambiar los nombres de las columnas
                venta_editar_df.columns = ["ID", "Fecha", "Producto Vendido", "Precio", "Metodo de Pago", "ID Usuario"]

                # Cambiar el orden del DataFrame
                venta_editar_df = venta_editar_df[["Producto Vendido", "Precio", "Metodo de Pago"]]

                st.dataframe(venta_editar_df)

                # Mostrar campos para editar cada variable
                for column in venta_editar_df.columns:
                    nuevo_valor = st.text_input(f"Nuevo valor para {column}", value=venta_editar_df.iloc[0][column])
                    venta_editar_df.at[0, column] = nuevo_valor

                # Botón para guardar los cambios
                if st.button("Guardar cambios"):
                    # Actualizar la venta en la base de datos
                    nueva_informacion = {
                        "productoVendido": venta_editar_df.at[0, "Producto Vendido"],
                        "precio": venta_editar_df.at[0, "Precio"],
                        "metodoPago": venta_editar_df.at[0, "Metodo de Pago"]
                    }

                    # Generar la sentencia SQL UPDATE
                    update_query = f"""
                        UPDATE Ventas
                        SET
                            productoVendido = '{nueva_informacion["productoVendido"]}',
                            precio = {nueva_informacion["precio"]},
                            metodoPago = '{nueva_informacion["metodoPago"]}'
                        WHERE idVenta = {id_venta_editar}
                    """

                    # Ejecutar la sentencia SQL UPDATE
                    cursor = db.cursor()
                    cursor.execute(update_query)
                    db.commit()

                    st.success("¡Venta actualizada correctamente!")

            else:
                st.warning(f"No se encontró ninguna venta con el ID {id_venta_editar}")

def main():
    visualiza_ventas()  # Mostrar sección de visualización para todos los usuarios

    editar_ventas()  # Mostrar sección de edición solo para admin

if __name__ == "__main__":
    main()
