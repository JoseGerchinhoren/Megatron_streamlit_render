import streamlit as st
import pyodbc
import json

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Función para insertar un pedido de arreglo técnico en la base de datos
def insertar_arreglo_tecnico(fecha, nombreCliente, contacto, modelo, falla, tipoDesbloqueo, imagenPatron, estado, observaciones, idUsuario):
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

        # Llamar a la stored procedure para insertar el pedido de arreglo técnico
        cursor.execute("EXEC InsertarArregloTecnico ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", 
                       (fecha, nombreCliente, contacto, modelo, falla, tipoDesbloqueo, imagenPatron, estado, observaciones, idUsuario))

        conn.commit()
        conn.close()
        st.success("Pedido de arreglo técnico registrado exitosamente")

    except Exception as e:
        st.error(f"Error al registrar el pedido de arreglo técnico: {e}")

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
    if st.button("Registrar Arreglo Técnico"):
        if fecha and nombreCliente and contacto and modelo and falla and estado:
            # Convertir la fecha a formato SQL Server (YYYY-MM-DD)
            fecha_sql = fecha.strftime('%Y-%m-%d')
            
            # Llamar a la función para insertar el arreglo técnico
            insertar_arreglo_tecnico(
                fecha_sql, nombreCliente, contacto, modelo, falla, tipoDesbloqueo,
                imagen_patron.read() if imagen_patron else None, estado, observaciones, idUsuario
            )
        else:
            st.warning("Por favor, complete todos los campos.")

if __name__ == "__main__":
    ingresa_arreglo_tecnico()
