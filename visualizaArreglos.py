import streamlit as st
import pandas as pd
from PIL import Image
import io

# Función para simular la obtención de datos de arreglos de servicio técnico
def obtener_datos_simulados():
    # Simular datos de arreglos de servicio técnico
    data = {
        "ID": [1, 2, 3],
        "Fecha": ["2023-01-01", "2023-02-01", "2023-03-01"],
        "Nombre del Cliente": ["Cliente1", "Cliente2", "Cliente3"],
        "Contacto": ["Contacto1", "Contacto2", "Contacto3"],
        "Modelo": ["Modelo1", "Modelo2", "Modelo3"],
        "Falla": ["Falla1", "Falla2", "Falla3"],
        "Estado": ["Avisado", "Entregado", "Señado"],
        "Contraseña Desbloqueo": ["1234", "5678", "0000"],
        "Observaciones": ["Obs1", "Obs2", "Obs3"],
        "Nombre de Usuario": ["Usuario1", "Usuario2", "Usuario3"],
    }

    # Crear un DataFrame simulado
    df = pd.DataFrame(data)

    return df

# Función para simular la obtención de una imagen de patrón de desbloqueo
def obtener_imagen_patron_simulada(id_arreglo):
    # Simular una imagen de patrón de desbloqueo
    imagen_patron_path = f"imagen_patron_{id_arreglo}.png"

    try:
        imagen_patron = Image.open(imagen_patron_path)
        return imagen_patron
    except FileNotFoundError:
        return None

# Función para simular la edición del estado de un arreglo
def editar_estado_arreglo_simulado(arreglos_df, id_arreglo, nuevo_estado):
    # Verificar si el ID del arreglo existe en los datos simulados
    if id_arreglo not in arreglos_df['ID'].values:
        st.warning(f"El ID del servicio técnico {id_arreglo} no existe.")
        return

    # Actualizar el estado del arreglo en los datos simulados
    arreglos_df.loc[arreglos_df['ID'] == id_arreglo, 'Estado'] = nuevo_estado

    st.success(f"Estado del servicio técnico {id_arreglo} editado correctamente a: {nuevo_estado}")

# Función principal para la interfaz de usuario
def visualizar_arreglos():
    st.title("Visualizar Arreglos de Servicio Técnico")

    # Obtener datos simulados
    arreglos_df = obtener_datos_simulados()

    # Cambiar los nombres de las columnas
    arreglos_df.columns = ["ID", "Fecha", "Nombre del Cliente", "Contacto", "Modelo", "Falla",
                           "Estado", "Contraseña Desbloqueo", "Observaciones", "Nombre de Usuario"]

    # Mostrar la tabla de arreglos de servicio técnico
    st.dataframe(arreglos_df)

    # Sección para ingresar el ID y mostrar la imagen del patrón de desbloqueo
    st.subheader("Visualizar Imagen de Patrón de Desbloqueo por ID")
    id_arreglo = st.number_input("Ingrese el ID del Arreglo:", value=0)

    # Obtener la imagen del patrón de desbloqueo simulada según el ID
    imagen_patron = obtener_imagen_patron_simulada(id_arreglo)

    # Mostrar la imagen si está disponible
    if imagen_patron is not None:
        st.image(imagen_patron, caption=f"Imagen del Patrón de Desbloqueo para el ID {id_arreglo}", width=400)
    else:
        st.warning(f"No se encontró ninguna imagen para el ID {id_arreglo}")

    # Sección para la edición del estado de registros simulada
    st.subheader("Editar Estado")
    id_arreglo_editar = st.number_input("Ingrese el ID del Arreglo que desea editar:", value=0)
    nuevo_estado = st.selectbox("Nuevo valor del campo estado:", ["Señado", "Pedido", "Avisado", "Entregado", "Cancelado"])

    if st.button("Guardar"):
        editar_estado_arreglo_simulado(arreglos_df, id_arreglo_editar, nuevo_estado)

# Función principal
def main():
    visualizar_arreglos()

if __name__ == "__main__":
    main()
