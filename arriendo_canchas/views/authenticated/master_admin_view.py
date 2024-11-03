# views/authenticated/master_admin_view.py

from views.authenticated.base_user_view import BaseUserView

def MasterAdminView(user_vm):
    base_view = BaseUserView(user_vm)
    # Aquí puedes añadir contenido específico para Master Admin
    return base_view
