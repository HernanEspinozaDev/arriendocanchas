# views/contact_us_view.py

import flet
from flet import Column, Container, ElevatedButton, Row, Text, TextField, alignment

def ContactUsView():
    nombre_field = TextField(label="Nombre")
    email_field = TextField(label="Email")
    asunto_field = TextField(label="Asunto")
    mensaje_field = TextField(label="Mensaje", multiline=True)

    def enviar_mensaje(e):
        # Lógica para enviar el mensaje
        print("Mensaje enviado")

    return Container(
        alignment=alignment.center,
        content=Column(
            alignment="center",
            controls=[
                Text("Contáctanos", size=32, weight="bold"),
                nombre_field,
                email_field,
                asunto_field,
                mensaje_field,
                ElevatedButton("Enviar Mensaje", on_click=enviar_mensaje),
            ],
        ),
    )
