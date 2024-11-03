# views/authenticated/empleado_atencion_view.py

from views.authenticated.base_user_view import BaseUserView

def EmpleadoAtencionView(user_vm):
    base_view = BaseUserView(user_vm)
    # Aquí puedes añadir contenido específico para Empleado de Atención
    return base_view
