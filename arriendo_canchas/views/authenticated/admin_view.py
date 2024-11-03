# views/authenticated/admin_view.py

from views.authenticated.base_user_view import BaseUserView

def AdminView(user_vm):
    base_view = BaseUserView(user_vm)
    # Aquí puedes añadir contenido específico para Administrador
    return base_view
