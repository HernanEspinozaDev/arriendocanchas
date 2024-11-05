# views/authenticated/cliente_arrendador_view.py

from flet import Column, Text

def ClienteArrendadorView(page, user_vm):
    user = user_vm.get_user()
    return Column(
        [
            Text(f"Bienvenido, {user['nombre']}", size=24, weight="bold"),
            Text("Esta es la vista para el Cliente Arrendador", size=18),
            # Contenido específico para Cliente Arrendador
        ]
    )
