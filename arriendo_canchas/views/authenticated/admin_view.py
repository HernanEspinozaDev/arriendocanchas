# views/authenticated/admin_view.py

from flet import Column, Text

def AdminView(page, user_vm):
    user = user_vm.get_user()
    return Column(
        [
            Text(f"Bienvenido, {user['nombre']}", size=24, weight="bold"),
            Text("Esta es la vista para el Administrador", size=18),
            # Contenido específico para Administrador
        ]
    )
