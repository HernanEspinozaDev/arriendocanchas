# arriendo_canchas/views/authenticated/atencion_view.py

from flet import (
    Column, Row, Text, ElevatedButton, TextField, DataTable, DataColumn,
    DataRow, DataCell, IconButton, icons, AlertDialog, TextButton
)
from models.usuario_model import UsuarioModel

def AtencionView(page, user_vm):
    usuario_model = UsuarioModel()

    # Obtener el id del usuario actual
    user = user_vm.get_user()
    id_usuario_actual = user['id_usuario']

    # Función para obtener empleados de atención
    def fetch_empleados():
        return usuario_model.fetch_usuarios(tipo_cuenta='EmpleadoAtencion')

    empleado_list = fetch_empleados()

    data_table = DataTable(
        columns=[
            DataColumn(Text("ID")),
            DataColumn(Text("Nombre")),
            DataColumn(Text("Correo")),
            DataColumn(Text("Acciones")),
        ],
        rows=[]
    )

    def create_data_row(empleado):
        return DataRow(
            cells=[
                DataCell(Text(str(empleado['id_usuario']))),
                DataCell(Text(empleado['nombre'])),
                DataCell(Text(empleado['correo'])),
                DataCell(
                    Row(
                        [
                            IconButton(icon=icons.EDIT, tooltip="Editar", on_click=lambda e, empleado=empleado: open_edit_dialog(empleado)),
                            IconButton(icon=icons.DELETE, tooltip="Eliminar", on_click=lambda e, empleado=empleado: open_delete_dialog(empleado)),
                        ]
                    )
                )
            ]
        )

    def refresh_data():
        empleado_list = fetch_empleados()
        data_table.rows = [create_data_row(empleado) for empleado in empleado_list]
        page.update()

    data_table.rows = [create_data_row(empleado) for empleado in empleado_list]

    # Funciones para agregar, editar y eliminar

    def open_add_dialog(e):
        rut_field = TextField(label="RUT")
        nombre_field = TextField(label="Nombre")
        apellido_paterno_field = TextField(label="Apellido Paterno")
        apellido_materno_field = TextField(label="Apellido Materno")
        telefono_field = TextField(label="Teléfono")
        correo_field = TextField(label="Correo")
        contrasena_field = TextField(label="Contraseña", password=True)

        def save_new_empleado(e):
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
                    tipo_cuenta='EmpleadoAtencion',
                    id_admin_responsable=id_usuario_actual
                )
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al agregar empleado de atención: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Agregar Empleado de Atención"),
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
                TextButton("Guardar", on_click=save_new_empleado),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    def open_edit_dialog(empleado):
        nombre_field = TextField(label="Nombre", value=empleado['nombre'])
        correo_field = TextField(label="Correo", value=empleado['correo'])

        def save_edit_empleado(e):
            nombre = nombre_field.value
            correo = correo_field.value
            id_usuario = empleado['id_usuario']

            try:
                usuario_model.update_usuario(id_usuario, nombre, correo)
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al editar empleado de atención: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Editar Empleado de Atención"),
            content=Column([
                nombre_field,
                correo_field,
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, 'open', False)),
                TextButton("Guardar", on_click=save_edit_empleado),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    def open_delete_dialog(empleado):
        def confirm_delete(e):
            id_usuario = empleado['id_usuario']
            try:
                usuario_model.delete_usuario(id_usuario)
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al eliminar empleado de atención: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Eliminar Empleado de Atención"),
            content=Text(f"¿Está seguro de eliminar al empleado {empleado['nombre']}?"),
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
                    Text("Gestionar Empleados de Atención", size=24, weight="bold"),
                    ElevatedButton("Agregar Empleado", on_click=open_add_dialog),
                ],
                alignment="spaceBetween",
            ),
            data_table,
        ]
    )
