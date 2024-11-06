# views/authenticated/buscar_complejos_view.py

from flet import (
    Column, TextField, ElevatedButton, DataTable, DataColumn, DataRow, DataCell, Text, Row, AlertDialog, TextButton
)
from models.complejo_model import ComplejoModel
from models.cancha_model import CanchaModel
from models.reserva_model import ReservaModel

def BuscarComplejosView(page, user_vm):
    complejo_model = ComplejoModel()
    cancha_model = CanchaModel()
    reserva_model = ReservaModel()
    id_usuario_actual = user_vm.get_user()['id_usuario']
    
    # Campo de búsqueda
    search_field = TextField(label="Buscar Complejo Deportivo")
    
    complejos_table = DataTable(
        columns=[
            DataColumn(Text("Nombre Complejo")),
            DataColumn(Text("Dirección")),
            DataColumn(Text("Acciones")),
        ],
        rows=[]
    )
    
    def buscar_complejos(e):
        termino = search_field.value
        complejos_list = complejo_model.fetch_complejos_by_name(termino)
        complejos_table.rows = [create_complejo_row(c) for c in complejos_list]
        page.update()
    
    def create_complejo_row(complejo):
        return DataRow(
            cells=[
                DataCell(Text(complejo['nombre_complejo'])),
                DataCell(Text(complejo['direccion'])),
                DataCell(
                    ElevatedButton("Ver Canchas", on_click=lambda e, complejo=complejo: ver_canchas(complejo))
                ),
            ]
        )
    
    def ver_canchas(complejo):
        # Mostrar las canchas del complejo
        query = """
        SELECT id_cancha, nombre_cancha, tipo_cancha
        FROM Canchas
        WHERE id_complejo = %s
        """
        cancha_model.cursor.execute(query, (complejo['id_complejo'],))
        canchas = cancha_model.cursor.fetchall()
        canchas_list = [{'id_cancha': c[0], 'nombre_cancha': c[1], 'tipo_cancha': c[2]} for c in canchas]
        
        canchas_table = DataTable(
            columns=[
                DataColumn(Text("Nombre Cancha")),
                DataColumn(Text("Tipo Cancha")),
                DataColumn(Text("Acciones")),
            ],
            rows=[DataRow(
                cells=[
                    DataCell(Text(c['nombre_cancha'])),
                    DataCell(Text(c['tipo_cancha'])),
                    DataCell(
                        ElevatedButton("Ver Disponibilidad", on_click=lambda e, cancha=c: ver_disponibilidad(cancha))
                    ),
                ]
            ) for c in canchas_list]
        )
        
        page.dialog = AlertDialog(
            title=Text(f"Canchas en {complejo['nombre_complejo']}"),
            content=canchas_table,
            actions=[
                TextButton("Cerrar", on_click=lambda e: setattr(page.dialog, 'open', False)),
            ],
            actions_alignment="end",
            fullscreen=True,
        )
        page.dialog.open = True
        page.update()
    
    def ver_disponibilidad(cancha):
        disponibilidad_list = cancha_model.fetch_disponibilidad(cancha['id_cancha'])
        disponibilidad_table = DataTable(
            columns=[
                DataColumn(Text("Fecha")),
                DataColumn(Text("Hora Inicio")),
                DataColumn(Text("Hora Fin")),
                DataColumn(Text("Acciones")),
            ],
            rows=[DataRow(
                cells=[
                    DataCell(Text(str(d['fecha']))),
                    DataCell(Text(str(d['hora_inicio']))),
                    DataCell(Text(str(d['hora_fin']))),
                    DataCell(
                        ElevatedButton("Reservar", on_click=lambda e, disponibilidad=d: reservar_cancha(disponibilidad))
                    ),
                ]
            ) for d in disponibilidad_list]
        )
        page.dialog = AlertDialog(
            title=Text(f"Disponibilidad de {cancha['nombre_cancha']}"),
            content=disponibilidad_table,
            actions=[
                TextButton("Cerrar", on_click=lambda e: setattr(page.dialog, 'open', False)),
            ],
            actions_alignment="end",
            fullscreen=True,
        )
        page.dialog.open = True
        page.update()
    
    def reservar_cancha(disponibilidad):
        id_usuario = id_usuario_actual
        id_cancha = disponibilidad['id_cancha']
        fecha_reserva = disponibilidad['fecha']
        hora_inicio = disponibilidad['hora_inicio']
        hora_fin = disponibilidad['hora_fin']
        id_disponibilidad = disponibilidad['id_disponibilidad']
        
        try:
            # Iniciar transacción
            cancha_model.db_service.connection.autocommit = False
            # Eliminar disponibilidad
            cancha_model.delete_disponibilidad(id_disponibilidad)
            # Agregar reserva
            reserva_model.add_reserva(id_usuario, id_cancha, fecha_reserva, hora_inicio, hora_fin)
            # Confirmar transacción
            cancha_model.db_service.connection.commit()
            cancha_model.db_service.connection.autocommit = True
            page.dialog = AlertDialog(
                title=Text("Reserva Exitosa"),
                content=Text(f"Ha reservado la cancha {disponibilidad['nombre_cancha']} el {fecha_reserva} de {hora_inicio} a {hora_fin}"),
                actions=[
                    TextButton("OK", on_click=lambda e: setattr(page.dialog, 'open', False)),
                ],
            )
            page.dialog.open = True
            # Actualizar disponibilidad
            ver_disponibilidad(cancha)
        except Exception as ex:
            cancha_model.db_service.connection.rollback()
            cancha_model.db_service.connection.autocommit = True
            print(f"Error al reservar cancha: {ex}")
            page.dialog = AlertDialog(
                title=Text("Error"),
                content=Text("No se pudo realizar la reserva. Por favor, inténtelo de nuevo."),
                actions=[
                    TextButton("OK", on_click=lambda e: setattr(page.dialog, 'open', False)),
                ],
            )
            page.dialog.open = True
            page.update()
    
    return Column(
        [
            Text("Buscar Complejos Deportivos", size=24, weight="bold"),
            Row(
                [
                    search_field,
                    ElevatedButton("Buscar", on_click=buscar_complejos),
                ]
            ),
            complejos_table,
        ]
    )
