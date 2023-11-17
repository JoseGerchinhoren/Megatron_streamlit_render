import streamlit as st
import pyodbc
import pandas as pd
import json
from PIL import Image
import io

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

def visualizar_arreglos():
    st.title("Visualizar Arreglos de Servicio Técnico")

    # Construir la consulta SQL para obtener los arreglos de servicio técnico
    query = "SELECT * FROM ArreglosTecnico ORDER BY idArreglo DESC"

    # Ejecutar la consulta y obtener los resultados en un DataFrame
    arreglos_df = pd.read_sql(query, db)

    # Consulta SQL para obtener la información de los usuarios
    query_usuarios = "SELECT idUsuario, nombreApellido FROM Usuarios"
    usuarios_df = pd.read_sql(query_usuarios, db)

    # Fusionar (unir) el DataFrame de arreglos con el DataFrame de usuarios
    arreglos_df = pd.merge(arreglos_df, usuarios_df, on="idUsuario", how="left")

    # Cambiar los nombres de las columnas
    arreglos_df.columns = ["ID", "Fecha", "Nombre del Cliente", "Contacto", "Modelo", "Falla", "Contraseña Desbloqueo", "Imagen Patrón", "Estado", "Observaciones", "ID Usuario", "Nombre de Usuario"]

    # Cambiar el orden del DataFrame
    arreglos_df = arreglos_df[[
        "ID",
        "Fecha",
        "Nombre del Cliente",
        "Contacto",
        "Modelo",
        "Falla",
        "Estado",
        "Contraseña Desbloqueo",
        "Observaciones",
        "Nombre de Usuario"
    ]]

    # Agregar un filtro por estado
    estados = arreglos_df['Estado'].unique()
    filtro_estado = st.selectbox("Filtrar por Estado:", ["Todos"] + list(estados))

    if filtro_estado != "Todos":
        arreglos_df = arreglos_df[arreglos_df['Estado'] == filtro_estado]

    # Mostrar la tabla de arreglos de servicio técnico
    st.dataframe(arreglos_df)

    # Sección para ingresar el ID y mostrar la imagen del patrón de desbloqueo
    st.subheader("Visualizar Imagen de Patrón de Desbloqueo por ID")
    id_arreglo = st.number_input("Ingrese el ID del Arreglo:", value=0)

    # Obtener la imagen del patrón de desbloqueo según el ID
    imagen_patron = obtener_imagen_patron(id_arreglo)

    # Mostrar la imagen si está disponible
    if imagen_patron is not None:
        st.image(imagen_patron, caption=f"Imagen del Patrón de Desbloqueo para el ID {id_arreglo}", width=400)
    else:
        st.warning(f"No se encontró ninguna imagen para el ID {id_arreglo}")

        # Sección para la edición del estado de registros
    st.subheader("Editar Estado")
    id_arreglo = st.number_input("Ingrese el ID del Pedido de Funda que desea editar:", value=0)
    nuevo_estado = st.selectbox("Nuevo valor del campo estado:", ["Señado", "Pedido", "Avisado","Entregado", "Cancelado"])

    if st.button("Guardar"):
        editar_estado_arreglo(arreglos_df, id_arreglo, nuevo_estado)

def obtener_imagen_patron(id_arreglo):
    try:
        # Construir la consulta SQL para obtener la imagen del patrón de desbloqueo por ID
        query = f"SELECT imagenPatron FROM ArreglosTecnico WHERE idArreglo = {id_arreglo}"
        
        # Ejecutar la consulta y obtener los resultados en un DataFrame
        result_df = pd.read_sql(query, db)

        # Obtener la imagen del patrón de desbloqueo (si está disponible)
        imagen_patron = result_df.at[0, 'imagenPatron'] if not result_df.empty else None

        return Image.open(io.BytesIO(imagen_patron)) if imagen_patron is not None else None
    except Exception as e:
        st.error(f"Error al obtener la imagen del patrón de desbloqueo: {e}")
        return None
    
def editar_estado_arreglo(arreglos_df, id_arreglo, nuevo_estado):
    try:
        # Crear un cursor para ejecutar comandos SQL
        cursor = db.cursor()

        # Verificar si el ID del arreglo
        if id_arreglo not in arreglos_df['idArreglo'].values:
            st.warning(f"El ID del servicio tecnico {id_arreglo} no existe.")
            return

        # Actualizar el estado del arreglo en la base de datos
        query = f"UPDATE ArreglosTecnico SET estado = '{nuevo_estado}' WHERE idArrego = {id_arreglo}"
        cursor.execute(query)
        db.commit()

        st.success(f"Estado del servicio tecnico {id_arreglo} editado correctamente a: {nuevo_estado}")

    except Exception as e:
        st.error(f"Error al editar el estado del servicio tecnico: {e}")

def main():
    visualizar_arreglos()

if __name__ == "__main__":
    main()
