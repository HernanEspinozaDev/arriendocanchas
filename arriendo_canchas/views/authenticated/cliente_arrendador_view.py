# views/authenticated/cliente_arrendador_view.py

from views.authenticated.base_user_view import BaseUserView

def ClienteArrendadorView(user_vm):
    base_view = BaseUserView(user_vm)
    # Aquí puedes añadir contenido específico para Cliente Arrendador
    return base_view
