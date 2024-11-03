# views/our_clients_view.py

import flet
from flet import Column, Container, Text, alignment

def OurClientsView():
    return Container(
        alignment=alignment.center,
        content=Column(
            alignment="center",
            controls=[
                Text("Nuestros Clientes", size=32, weight="bold"),
                Text(
                    "Aquí puedes mostrar testimonios o logos de tus clientes.",
                    size=16,
                    text_align="center"
                ),
                # Puedes agregar más elementos aquí si lo deseas
            ],
        ),
    )
