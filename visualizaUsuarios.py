import streamlit as st
import pyodbc
import pandas as pd
import json

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

def visualizar_usuarios():
    st.title("Visualizar Usuarios")

    # Consulta SQL para obtener la información de los usuarios
    query_usuarios = "SELECT * FROM Usuarios"
    usuarios_df = pd.read_sql(query_usuarios, db)

    # Cambiar los nombres de las columnas según tus necesidades
    usuarios_df.columns = ["ID", "Nombre y Apellido", "Correo Electrónico", "Contraseña", "Fecha de Nacimiento", "DNI", "Domicilio",  "Fecha Creacion", "Rol"]

    # Quita columna Contraseña
    usuarios_df = usuarios_df[[
        "ID", "Nombre y Apellido", "Correo Electrónico", "Fecha de Nacimiento", "DNI", "Domicilio",  "Fecha Creacion", "Rol"
    ]]

#idUsuario	nombreApellido	email	contraseña	fechaNacimiento	dni	domicilio	fechaCreacion	rol

    # Mostrar la tabla de usuarios
    st.dataframe(usuarios_df)

def editar_usuarios():
    st.title("Editar Usuarios")

    # Agregar un campo para ingresar el idUsuario
    id_usuario_editar = st.text_input("Ingrese el ID del usuario que desea editar:")

    if id_usuario_editar:
        # Consultar el usuario específico por ID
        query_usuario = f"SELECT * FROM Usuarios WHERE idUsuario = {id_usuario_editar}"
        usuario_editar_df = pd.read_sql(query_usuario, db)

        if not usuario_editar_df.empty:
            # Mostrar la información actual de la venta
            st.write("Información actual de la venta:")
            # Cambiar los nombres de las columnas
            usuario_editar_df.columns = ["ID", "Nombre y Apellido", "Correo Electrónico", "Contraseña", "Fecha de Nacimiento", "DNI", "Domicilio",  "Fecha Creacion", "Rol"]

            # Cambiar el orden del DataFrame
            usuario_editar_df = usuario_editar_df[[
                "Nombre y Apellido", "Correo Electrónico", "Fecha de Nacimiento", "DNI", "Domicilio", "Rol"
                ]]

            st.dataframe(usuario_editar_df)

            # Mostrar campos para editar cada variable
            for column in usuario_editar_df.columns:
                nuevo_valor = st.text_input(f"Nuevo valor para {column}", value=usuario_editar_df.iloc[0][column])
                usuario_editar_df.at[0, column] = nuevo_valor

            # Botón para guardar los cambios
            if st.button("Guardar cambios"):
                # Actualizar la venta en la base de datos
                nueva_informacion = {
                    "nombreApellido": usuario_editar_df.at[0, "Nombre y Apellido"],
                    "email": usuario_editar_df.at[0, "Correo Electrónico"],
                    "fechaNacimiento": usuario_editar_df.at[0, "Fecha de Nacimiento"],
                    "dni": usuario_editar_df.at[0, "DNI"],
                    "domicilio": usuario_editar_df.at[0, "Domicilio"],
                    "rol": usuario_editar_df.at[0, "Rol"]
                }

                # Generar la sentencia SQL UPDATE
                update_query = f"""
                    UPDATE Usuarios
                    SET
                        nombreApellido = '{nueva_informacion["nombreApellido"]}',
                        email = '{nueva_informacion["email"]}',
                        fechaNacimiento = {nueva_informacion["fechaNacimiento"]},
                        dni = '{nueva_informacion["dni"]}',
                        domicilio = {nueva_informacion["domicilio"]}
                    WHERE idUsuario = {id_usuario_editar}
                """

                # Ejecutar la sentencia SQL UPDATE
                cursor = db.cursor()
                cursor.execute(update_query)
                db.commit()

                st.success("Usuario actualizado correctamente!")

        else:
            st.warning(f"No se encontró ningun usuario con el ID {id_usuario_editar}")

def main():
    visualizar_usuarios()  # Mostrar sección de visualización de usuarios

    # Verificar si el usuario es admin
    if st.session_state.user_rol == "admin":
        editar_usuarios()  # Mostrar sección de edición solo para admin

if __name__ == "__main__":
    main()
