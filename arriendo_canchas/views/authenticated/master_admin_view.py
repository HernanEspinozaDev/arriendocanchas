# views/authenticated/master_admin_view.py

from flet import Column, Text, ElevatedButton, Row

def MasterAdminView(page, user_vm):
    user = user_vm.get_user()
    return Column(
        [
            Text(f"Bienvenido, {user['nombre']}", size=24, weight="bold"),
            Text("Esta es la vista para el Master Admin", size=18),
            # Aquí puedes añadir más contenido específico para Master Admin
        ]
    )
