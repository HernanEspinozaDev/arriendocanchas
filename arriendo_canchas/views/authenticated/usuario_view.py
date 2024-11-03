# views/authenticated/usuario_view.py

from views.authenticated.base_user_view import BaseUserView

def UsuarioView(user_vm):
    base_view = BaseUserView(user_vm)
    # Aquí puedes añadir contenido específico para Usuario
    return base_view
