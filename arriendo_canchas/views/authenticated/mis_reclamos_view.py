# views/authenticated/mis_reclamos_view.py

from flet import (
    Column, DataTable, DataColumn, DataRow, DataCell, Text, ElevatedButton, TextField, Dropdown, dropdown, AlertDialog, TextButton
)
from models.reclamo_model import ReclamoModel
from models.reserva_model import ReservaModel

def MisReclamosView(page, user_vm):
    reclamo_model = ReclamoModel()
    reserva_model = ReservaModel()
    id_usuario = user_vm.get_user()['id_usuario']
    rut_cliente = user_vm.get_user()['rut']
    
    reclamos_list = reclamo_model.fetch_reclamos(id_usuario)
    
    reclamos_table = DataTable(
        columns=[
            DataColumn(Text("Cancha")),
            DataColumn(Text("Fecha Reserva")),
            DataColumn(Text("Tipo Reclamo")),
            DataColumn(Text("Estado")),
        ],
        rows=[DataRow(
            cells=[
                DataCell(Text(r['nombre_cancha'])),
                DataCell(Text(str(r['fecha_reserva']))),
                DataCell(Text(r['tipo_reclamo'])),
                DataCell(Text(r['estado'])),
            ]
        ) for r in reclamos_list]
    )
    
    def open_add_reclamo_dialog(e):
        # Obtener reservas del usuario
        reservas_list = reserva_model.fetch_reservas(id_usuario)
        reserva_options = [dropdown.Option(str(r['id_reserva']), f"{r['nombre_cancha']} - {r['fecha_reserva']}") for r in reservas_list]
        
        reserva_dropdown = Dropdown(
            label="Reserva",
            options=reserva_options
        )
        tipo_reclamo_field = TextField(label="Tipo de Reclamo")
        
        def save_new_reclamo(e):
            id_reserva = int(reserva_dropdown.value)
            tipo_reclamo = tipo_reclamo_field.value
            try:
                reclamo_model.add_reclamo(id_reserva, rut_cliente, tipo_reclamo)
                page.dialog.open = False
                # Refrescar la lista de reclamos
                reclamos_list[:] = reclamo_model.fetch_reclamos(id_usuario)
                reclamos_table.rows = [DataRow(
                    cells=[
                        DataCell(Text(r['nombre_cancha'])),
                        DataCell(Text(str(r['fecha_reserva']))),
                        DataCell(Text(r['tipo_reclamo'])),
                        DataCell(Text(r['estado'])),
                    ]
                ) for r in reclamos_list]
                page.update()
            except Exception as ex:
                print(f"Error al agregar reclamo: {ex}")
                page.dialog.open = False
        
        page.dialog = AlertDialog(
            title=Text("Agregar Reclamo"),
            content=Column([
                reserva_dropdown,
                tipo_reclamo_field,
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, 'open', False)),
                TextButton("Guardar", on_click=save_new_reclamo),
            ],
            actions_alignment="end",
        )
        page.dialog.open = True
        page.update()
    
    return Column(
        [
            Text("Mis Reclamos", size=24, weight="bold"),
            ElevatedButton("Agregar Reclamo", on_click=open_add_reclamo_dialog),
            reclamos_table,
        ]
    )
