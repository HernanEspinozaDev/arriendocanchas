# views/authenticated/base_user_view.py

import flet
from flet import Column, Text, alignment

def BaseUserView(user_vm):
    user = user_vm.get_user()
    return Column(
        [
            Text(f"Bienvenido, {user['nombre']}", size=24, weight="bold"),
            Text(f"Tipo de Usuario: {user['tipo_cuenta']}", size=18),
            # Aquí puedes añadir contenido común
        ],
        alignment="center",
        horizontal_alignment="center",
    )
