# views/authenticated/empleado_atencion_view.py

from flet import Column, Text

def EmpleadoAtencionView(page, user_vm):
    user = user_vm.get_user()
    return Column(
        [
            Text(f"Bienvenido, {user['nombre']}", size=24, weight="bold"),
            Text("Esta es la vista para el Empleado de Atención", size=18),
            # Contenido específico para Empleado de Atención
        ]
    )
