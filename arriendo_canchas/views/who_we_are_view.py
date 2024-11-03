# views/who_we_are_view.py

import flet
from flet import Column, Container, Text, alignment

def WhoWeAreView():
    return Container(
        alignment=alignment.center,
        content=Column(
            alignment="center",
            controls=[
                Text("Quiénes Somos", size=32, weight="bold"),
                Text(
                    "Somos una plataforma dedicada a la administración eficiente de canchas deportivas.",
                    size=16
                ),
                # Agrega más elementos si es necesario
            ],
        ),
    )
