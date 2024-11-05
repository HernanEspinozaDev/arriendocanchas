# arriendo_canchas/views/authenticated/canchas_view.py

from flet import (
    Column, Row, Text, ElevatedButton, TextField, DataTable, DataColumn,
    DataRow, DataCell, IconButton, icons, AlertDialog, TextButton, Dropdown, dropdown
)
from services.database_service import DatabaseService

def CanchasView(page, user_vm):
    db_service = DatabaseService()
    cursor = db_service.cursor

    # Obtener el id del usuario actual
    user = user_vm.get_user()
    user_id = user['id_usuario']

    # Función para obtener canchas del arrendador
    def fetch_canchas():
        query = """
        SELECT c.id_cancha, c.nombre_cancha, c.tipo_cancha, co.nombre_complejo
        FROM Canchas c
        JOIN ComplejosDeportivos co ON c.id_complejo = co.id_complejo
        WHERE co.id_usuario = %s
        """
        cursor.execute(query, (user_id,))
        canchas = cursor.fetchall()
        return [{'id_cancha': c[0], 'nombre_cancha': c[1], 'tipo_cancha': c[2], 'complejo_nombre': c[3]} for c in canchas]

    cancha_list = fetch_canchas()

    data_table = DataTable(
        columns=[
            DataColumn(Text("ID")),
            DataColumn(Text("Nombre Cancha")),
            DataColumn(Text("Tipo Cancha")),
            DataColumn(Text("Complejo")),
            DataColumn(Text("Acciones")),
        ],
        rows=[]
    )

    def create_data_row(cancha):
        return DataRow(
            cells=[
                DataCell(Text(str(cancha['id_cancha']))),
                DataCell(Text(cancha['nombre_cancha'])),
                DataCell(Text(cancha['tipo_cancha'])),
                DataCell(Text(cancha['complejo_nombre'])),
                DataCell(
                    Row(
                        [
                            IconButton(icon=icons.EDIT, tooltip="Editar", on_click=lambda e, cancha=cancha: open_edit_dialog(cancha)),
                            IconButton(icon=icons.DELETE, tooltip="Eliminar", on_click=lambda e, cancha=cancha: open_delete_dialog(cancha)),
                        ]
                    )
                )
            ]
        )

    def refresh_data():
        cancha_list = fetch_canchas()
        data_table.rows = [create_data_row(cancha) for cancha in cancha_list]
        page.update()

    data_table.rows = [create_data_row(cancha) for cancha in cancha_list]

    # Obtener lista de complejos del arrendador
    def fetch_complejos():
        query = """
        SELECT id_complejo, nombre_complejo 
        FROM ComplejosDeportivos 
        WHERE id_usuario = %s
        """
        cursor.execute(query, (user_id,))
        complejos = cursor.fetchall()
        return [{'id_complejo': c[0], 'nombre_complejo': c[1]} for c in complejos]

    complejos_list = fetch_complejos()

    # Funciones para agregar, editar y eliminar

    def open_add_dialog(e):
        nombre_field = TextField(label="Nombre Cancha")
        tipo_field = TextField(label="Tipo Cancha")
        complejo_dropdown = Dropdown(
            label="Complejo Deportivo",
            options=[dropdown.Option(str(c['id_complejo']), c['nombre_complejo']) for c in complejos_list]
        )

        def save_new_cancha(e):
            nombre = nombre_field.value
            tipo = tipo_field.value
            id_complejo = int(complejo_dropdown.value)

            # Insertar en la base de datos
            try:
                query = """
                INSERT INTO Canchas (nombre_cancha, tipo_cancha, id_complejo)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (nombre, tipo, id_complejo))
                db_service.connection.commit()
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al agregar cancha: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Agregar Cancha"),
            content=Column([
                nombre_field,
                tipo_field,
                complejo_dropdown,
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, 'open', False)),
                TextButton("Guardar", on_click=save_new_cancha),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    def open_edit_dialog(cancha):
        nombre_field = TextField(label="Nombre Cancha", value=cancha['nombre_cancha'])
        tipo_field = TextField(label="Tipo Cancha", value=cancha['tipo_cancha'])
        complejo_dropdown = Dropdown(
            label="Complejo Deportivo",
            options=[dropdown.Option(str(c['id_complejo']), c['nombre_complejo']) for c in complejos_list],
            value=str(next(c['id_complejo'] for c in complejos_list if c['nombre_complejo'] == cancha['complejo_nombre']))
        )

        def save_edit_cancha(e):
            nombre = nombre_field.value
            tipo = tipo_field.value
            id_complejo = int(complejo_dropdown.value)
            cancha_id = cancha['id_cancha']

            try:
                query = """
                UPDATE Canchas 
                SET nombre_cancha = %s, tipo_cancha = %s, id_complejo = %s 
                WHERE id_cancha = %s
                """
                cursor.execute(query, (nombre, tipo, id_complejo, cancha_id))
                db_service.connection.commit()
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al editar cancha: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Editar Cancha"),
            content=Column([
                nombre_field,
                tipo_field,
                complejo_dropdown,
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, 'open', False)),
                TextButton("Guardar", on_click=save_edit_cancha),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()

    def open_delete_dialog(cancha):
        def confirm_delete(e):
            cancha_id = cancha['id_cancha']
            try:
                query = "DELETE FROM Canchas WHERE id_cancha = %s"
                cursor.execute(query, (cancha_id,))
                db_service.connection.commit()
                page.dialog.open = False
                refresh_data()
            except Exception as ex:
                print(f"Error al eliminar cancha: {ex}")
                page.dialog.open = False

        page.dialog = AlertDialog(
            title=Text("Eliminar Cancha"),
            content=Text(f"¿Está seguro de eliminar la cancha {cancha['nombre_cancha']}?"),
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
                    Text("Gestionar Canchas", size=24, weight="bold"),
                    ElevatedButton("Agregar Cancha", on_click=open_add_dialog),
                ],
                alignment="spaceBetween",
            ),
            data_table,
        ]
    )
