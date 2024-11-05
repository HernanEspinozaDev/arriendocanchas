# arriendo_canchas/views/authenticated/usuarios_view.py

from flet import (
    Column, Row, Text, ElevatedButton, TextField, DataTable, DataColumn,
    DataRow, DataCell, IconButton, icons, AlertDialog, TextButton
)
from models.usuario_model import UsuarioModel

def UsuariosView(page, user_vm):
    usuario_model = UsuarioModel()

    # Obtener el id del usuario actual
    user = user_vm.get_user()
    id_usuario_actual = user['id_usuario']

    # Función para obtener usuarios
    def fetch_usuarios():
        return usuario_model.fetch_usuarios(tipo_cuenta='Usuario')

    usuario_list = fetch_usuarios()

    data_table = DataTable(
        columns=[
            DataColumn(Text("ID")),
            DataColumn(Text("Nombre")),
            DataColumn(Text("Correo")),
            DataColumn(Text("Acciones")),
        ],
        rows=[]
    )

    def create_data_row(usuario):
        return DataRow(
            cells=[
                DataCell(Text(str(usuario['id_usuario']))),
                DataCell(Text(usuario['nombre'])),
                DataCell(Text(usuario['correo'])),
                DataCell(
                    Row(
                        [
                            IconButton(
                                icon=icons.EDIT, 
                                tooltip="Editar", 
                                on_click=lambda e, usuario=usuario: open_edit_dialog(usuario)
                            ),
                            IconButton(
                                icon=icons.DELETE, 
                                tooltip="Eliminar", 
                                on_click=lambda e, usuario=usuario: open_delete_dialog(usuario)
                            ),
                        ]
                    )
                )
            ]
        )

    def refresh_data():
        usuario_list = fetch_usuarios()
        data_table.rows = [create_data_row(usuario) for usuario in usuario_list]
        page.update()

    data_table.rows = [create_data_row(usuario) for usuario in usuario_list]

    # Funciones para agregar, editar y eliminar

    def open_add_dialog(e):
        rut_field = TextField(label="RUT")
        nombre_field = TextField(label="Nombre")
        apellido_paterno_field = TextField(label="Apellido Paterno")
        apellido_materno_field = TextField(label="Apellido Materno")
        telefono_field = TextField(label="Teléfono")
        correo_field = TextField(label="Correo")
        contrasena_field = TextField(label="Contraseña", password=True)

        def save_new_usuario(e):
            rut = rut_field.value
            nombre = nombre_field.value
            apellido_paterno = apellido_paterno_field.value
            apellido_materno = apellido_materno_field.value
            telefono = telefono_field.value
            correo = correo_field.value
            contrasena = contrasena_field.value

            # Insertar en la base de datos
            try:
                usuario_model.add_usuario(
                    rut=rut,
                    nombre=nombre,
                    apellido_paterno=apellido_paterno,
                    apellido_materno=apellido_materno,
                    telefono=telefono,
                    correo=correo,
                    contrasena=contrasena,
                    tipo_cuenta='Usuario'
                )
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al agregar usuario: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Agregar Usuario"),
            content=Column([
                rut_field,
                nombre_field,
                apellido_paterno_field,
                apellido_materno_field,
                telefono_field,
                correo_field,
                contrasena_field,
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, 'open', False)),
                TextButton("Guardar", on_click=save_new_usuario),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    def open_edit_dialog(usuario):
        nombre_field = TextField(label="Nombre", value=usuario['nombre'])
        apellido_paterno_field = TextField(label="Apellido Paterno", value="")  # Puedes ajustar esto
        apellido_materno_field = TextField(label="Apellido Materno", value="")  # Puedes ajustar esto
        telefono_field = TextField(label="Teléfono", value="")  # Puedes ajustar esto
        correo_field = TextField(label="Correo", value=usuario['correo'])

        def save_edit_usuario(e):
            nombre = nombre_field.value
            apellido_paterno = apellido_paterno_field.value
            apellido_materno = apellido_materno_field.value
            telefono = telefono_field.value
            correo = correo_field.value
            id_usuario = usuario['id_usuario']

            try:
                # Actualizar nombre, correo y otros campos según sea necesario
                # Si deseas actualizar otros campos como rut, apellido, teléfono, deberás ajustar el modelo y la vista
                usuario_model.update_usuario(id_usuario, nombre, correo)
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al editar usuario: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Editar Usuario"),
            content=Column([
                nombre_field,
                apellido_paterno_field,
                apellido_materno_field,
                telefono_field,
                correo_field,
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, 'open', False)),
                TextButton("Guardar", on_click=save_edit_usuario),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    def open_delete_dialog(usuario):
        def confirm_delete(e):
            id_usuario = usuario['id_usuario']
            try:
                usuario_model.delete_usuario(id_usuario)
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al eliminar usuario: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Eliminar Usuario"),
            content=Text(f"¿Está seguro de eliminar al usuario {usuario['nombre']}?"),
            actions=[
                TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, 'open', False)),
                TextButton("Eliminar", on_click=confirm_delete),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    return Column(
        [
            Row(
                [
                    Text("Gestionar Usuarios", size=24, weight="bold"),
                    ElevatedButton("Agregar Usuario", on_click=open_add_dialog),
                ],
                alignment="spaceBetween",
            ),
            data_table,
        ]
    )
