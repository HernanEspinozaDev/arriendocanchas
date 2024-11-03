# views/authenticated/coordinador_personal_view.py

from views.authenticated.base_user_view import BaseUserView

def CoordinadorPersonalView(user_vm):
    base_view = BaseUserView(user_vm)
    # Aquí puedes añadir contenido específico para Coordinador Personal
    return base_view
