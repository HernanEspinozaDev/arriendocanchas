# views/authenticated/coordinador_personal_view.py

from flet import Column, Text

def CoordinadorPersonalView(page, user_vm):
    user = user_vm.get_user()
    return Column(
        [
            Text(f"Bienvenido, {user['nombre']}", size=24, weight="bold"),
            Text("Esta es la vista para el Coordinador de Personal", size=18),
            # Contenido específico para Coordinador de Personal
        ]
    )
