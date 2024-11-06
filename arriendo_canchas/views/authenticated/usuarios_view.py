# arriendo_canchas/views/authenticated/usuarios_view.py

from flet import (
    Column, Row, Text, ElevatedButton, TextField, DataTable, DataColumn,
    DataRow, DataCell, AlertDialog, TextButton
)
from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.cancha_model import CanchaModel

def UsuariosView(page, user_vm):
    usuario_model = UsuarioModel()
    reserva_model = ReservaModel()
    cancha_model = CanchaModel()
    
    # Obtener el usuario actual
    user = user_vm.get_user()
    id_usuario_actual = user['id_usuario']
    
    # Campo de fecha para buscar
    fecha_field = TextField(label="Fecha (YYYY-MM-DD)")
    
    # Función para buscar canchas disponibles
    def buscar_canchas(e):
        fecha = fecha_field.value
        if not fecha:
            page.dialog = AlertDialog(
                title=Text("Error"),
                content=Text("Por favor, ingrese una fecha"),
                actions=[
                    TextButton("OK", on_click=lambda e: setattr(page.dialog, 'open', False)),
                ],
            )
            page.dialog.open = True
            page.update()
            return
        disponibilidad_list = fetch_disponibilidad_por_fecha(fecha)
        disponibilidad_table.rows = [create_disponibilidad_row(d) for d in disponibilidad_list]
        page.update()
    
    def fetch_disponibilidad_por_fecha(fecha):
        query = """
        SELECT dc.id_disponibilidad, c.nombre_cancha, co.nombre_complejo, dc.fecha, dc.hora_inicio, dc.hora_fin, c.id_cancha
        FROM DisponibilidadCanchas dc
        JOIN Canchas c ON dc.id_cancha = c.id_cancha
        JOIN ComplejosDeportivos co ON c.id_complejo = co.id_complejo
        WHERE dc.fecha = %s
        """
        cancha_model.cursor.execute(query, (fecha,))
        disponibilidad = cancha_model.cursor.fetchall()
        return [{
            'id_disponibilidad': d[0],
            'nombre_cancha': d[1],
            'nombre_complejo': d[2],
            'fecha': d[3],
            'hora_inicio': d[4],
            'hora_fin': d[5],
            'id_cancha': d[6]
        } for d in disponibilidad]
    
    disponibilidad_table = DataTable(
        columns=[
            DataColumn(Text("Cancha")),
            DataColumn(Text("Complejo")),
            DataColumn(Text("Fecha")),
            DataColumn(Text("Hora Inicio")),
            DataColumn(Text("Hora Fin")),
            DataColumn(Text("Acciones")),
        ],
        rows=[]
    )
    
    def create_disponibilidad_row(disponibilidad):
        return DataRow(
            cells=[
                DataCell(Text(disponibilidad['nombre_cancha'])),
                DataCell(Text(disponibilidad['nombre_complejo'])),
                DataCell(Text(str(disponibilidad['fecha']))),
                DataCell(Text(str(disponibilidad['hora_inicio']))),
                DataCell(Text(str(disponibilidad['hora_fin']))),
                DataCell(
                    Row(
                        [
                            ElevatedButton("Reservar", on_click=lambda e, disponibilidad=disponibilidad: reservar_cancha(disponibilidad)),
                        ]
                    )
                )
            ]
        )
    
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
            # Eliminar disponibilidad para evitar reservas duplicadas
            cancha_model.delete_disponibilidad(id_disponibilidad)
            # Agregar reserva
            reserva_model.add_reserva(id_usuario, id_cancha, fecha_reserva, hora_inicio, hora_fin)
            # Confirmar transacción
            cancha_model.db_service.connection.commit()
            cancha_model.db_service.connection.autocommit = True
            page.dialog = AlertDialog(
                title=Text("Reserva Exitosa"),
                content=Text(f"Ha reservado la cancha {disponibilidad['nombre_cancha']} en el complejo {disponibilidad['nombre_complejo']} el {fecha_reserva} de {hora_inicio} a {hora_fin}"),
                actions=[
                    TextButton("OK", on_click=lambda e: setattr(page.dialog, 'open', False)),
                ],
            )
            page.dialog.open = True
            # Actualizar tabla de disponibilidad
            buscar_canchas(None)
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
            Text("Reservar Canchas", size=24, weight="bold"),
            Row(
                [
                    fecha_field,
                    ElevatedButton("Buscar Canchas Disponibles", on_click=buscar_canchas),
                ]
            ),
            disponibilidad_table,
        ]
    )
