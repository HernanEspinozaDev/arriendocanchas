# views/authenticated/usuario_view.py

from flet import Column, Text

def UsuarioView(page, user_vm):
    user = user_vm.get_user()
    return Column(
        [
            Text(f"Bienvenido, {user['nombre']}", size=24, weight="bold"),
            Text("Esta es la vista para el Usuario", size=18),
            # Contenido específico para Usuario
        ]
    )
