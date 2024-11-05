# arriendo_canchas/views/authenticated/coordinadores_view.py

from flet import (
    Column, Row, Text, ElevatedButton, TextField, DataTable, DataColumn,
    DataRow, DataCell, IconButton, icons, AlertDialog, TextButton
)
from models.usuario_model import UsuarioModel

def CoordinadoresView(page, user_vm):
    usuario_model = UsuarioModel()

    # Obtener el id del usuario actual
    user = user_vm.get_user()
    id_usuario_actual = user['id_usuario']

    # Función para obtener coordinadores
    def fetch_coordinadores():
        return usuario_model.fetch_usuarios(tipo_cuenta='CoordinadorPersonal')

    coordinador_list = fetch_coordinadores()

    data_table = DataTable(
        columns=[
            DataColumn(Text("ID")),
            DataColumn(Text("Nombre")),
            DataColumn(Text("Correo")),
            DataColumn(Text("Acciones")),
        ],
        rows=[]
    )

    def create_data_row(coordinador):
        return DataRow(
            cells=[
                DataCell(Text(str(coordinador['id_usuario']))),
                DataCell(Text(coordinador['nombre'])),
                DataCell(Text(coordinador['correo'])),
                DataCell(
                    Row(
                        [
                            IconButton(icon=icons.EDIT, tooltip="Editar", on_click=lambda e, coordinador=coordinador: open_edit_dialog(coordinador)),
                            IconButton(icon=icons.DELETE, tooltip="Eliminar", on_click=lambda e, coordinador=coordinador: open_delete_dialog(coordinador)),
                        ]
                    )
                )
            ]
        )

    def refresh_data():
        coordinador_list = fetch_coordinadores()
        data_table.rows = [create_data_row(coordinador) for coordinador in coordinador_list]
        page.update()

    data_table.rows = [create_data_row(coordinador) for coordinador in coordinador_list]

    # Funciones para agregar, editar y eliminar

    def open_add_dialog(e):
        rut_field = TextField(label="RUT")
        nombre_field = TextField(label="Nombre")
        apellido_paterno_field = TextField(label="Apellido Paterno")
        apellido_materno_field = TextField(label="Apellido Materno")
        telefono_field = TextField(label="Teléfono")
        correo_field = TextField(label="Correo")
        contrasena_field = TextField(label="Contraseña", password=True)

        def save_new_coordinador(e):
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
                    tipo_cuenta='CoordinadorPersonal',
                    id_admin_responsable=id_usuario_actual
                )
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al agregar coordinador: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Agregar Coordinador Personal"),
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
                TextButton("Guardar", on_click=save_new_coordinador),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    def open_edit_dialog(coordinador):
        nombre_field = TextField(label="Nombre", value=coordinador['nombre'])
        correo_field = TextField(label="Correo", value=coordinador['correo'])

        def save_edit_coordinador(e):
            nombre = nombre_field.value
            correo = correo_field.value
            id_usuario = coordinador['id_usuario']

            try:
                usuario_model.update_usuario(id_usuario, nombre, correo)
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al editar coordinador: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Editar Coordinador Personal"),
            content=Column([
                nombre_field,
                correo_field,
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, 'open', False)),
                TextButton("Guardar", on_click=save_edit_coordinador),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    def open_delete_dialog(coordinador):
        def confirm_delete(e):
            id_usuario = coordinador['id_usuario']
            try:
                usuario_model.delete_usuario(id_usuario)
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al eliminar coordinador: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Eliminar Coordinador Personal"),
            content=Text(f"¿Está seguro de eliminar al coordinador {coordinador['nombre']}?"),
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
                    Text("Gestionar Coordinadores Personales", size=24, weight="bold"),
                    ElevatedButton("Agregar Coordinador", on_click=open_add_dialog),
                ],
                alignment="spaceBetween",
            ),
            data_table,
        ]
    )
