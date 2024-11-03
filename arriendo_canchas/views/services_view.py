# views/services_view.py

import flet
from flet import Column, Container, Icon, Row, Text, alignment, icons

def ServicesView():
    return Container(
        alignment=alignment.center,
        content=Column(
            alignment="center",
            controls=[
                Text("Nuestros Servicios", size=32, weight="bold"),
                Row(
                    alignment="center",
                    controls=[
                        _build_service_item(icons.EVENT_AVAILABLE, "Gestión de Reservas", "Sistema de reservas en línea fácil de usar."),
                        _build_service_item(icons.PEOPLE, "Gestión de Clientes", "Administra fácilmente tus clientes y sus reservas."),
                        _build_service_item(icons.PAYMENT, "Pagos en Línea", "Procesa pagos de forma segura y eficiente."),
                    ],
                ),
            ],
        ),
    )

def _build_service_item(icon, title, description):
    return Column(
        alignment="center",
        controls=[
            Icon(name=icon, size=40),
            Text(title, size=20, weight="bold"),
            Text(description, size=16, text_align="center"),
        ],
    )
