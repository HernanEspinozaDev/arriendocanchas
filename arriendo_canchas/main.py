# main.py

import flet
from flet import Page, Text, Column, Row, Container
from views.home_view import HomeView
from views.login_view import LoginView
from views.widgets.navbar import Navbar as LandingNavbar
from views.widgets.navbar_pages import Navbar as AuthenticatedNavbar
from views.widgets.sidebar import Sidebar
from viewmodels.user_viewmodel import UserViewModel
from views.authenticated.admin_view import AdminView
from views.authenticated.cliente_arrendador_view import ClienteArrendadorView
from views.authenticated.usuario_view import UsuarioView
from views.authenticated.coordinador_personal_view import CoordinadorPersonalView
from views.authenticated.empleado_atencion_view import EmpleadoAtencionView
from views.authenticated.master_admin_view import MasterAdminView

def main(page: Page):
    page.title = "ArriendoCancha.cl"
    page.theme_mode = "light"
    page.vertical_alignment = "start"

    user_vm = UserViewModel()

    # Inicializar page.section_ids con la sección de login incluida
    page.section_ids = {
        "home": "home_section",
        "about": "about_section",
        "services": "services_section",
        "clients": "clients_section",
        "contact": "contact_section",
        "login": "login_section"  # Agregar login aquí
    }

    # Estado para controlar la visibilidad del sidebar
    sidebar_visible = False

    # Función para alternar la visibilidad del sidebar
    def toggle_sidebar(e):
        nonlocal sidebar_visible
        sidebar_visible = not sidebar_visible
        route_change(page.route)

    # Función para manejar rutas
    def route_change(route):
        page.controls.clear()
        if user_vm.is_authenticated():
            # Usuario autenticado
            user_type = user_vm.get_user()['tipo_cuenta']
            page.appbar = AuthenticatedNavbar(page, user_vm, toggle_sidebar)
            if page.route == "/dashboard" or page.route == "/":
                # Seleccionar la vista según el tipo de usuario
                if user_type == "Administrador":
                    content = AdminView(user_vm)
                elif user_type == "ClienteArrendador":
                    content = ClienteArrendadorView(user_vm)
                elif user_type == "Usuario":
                    content = UsuarioView(user_vm)
                elif user_type == "CoordinadorPersonal":
                    content = CoordinadorPersonalView(user_vm)
                elif user_type == "EmpleadoAtencion":
                    content = EmpleadoAtencionView(user_vm)
                elif user_type == "MasterAdmin":
                    content = MasterAdminView(user_vm)
                else:
                    content = Text("Tipo de usuario desconocido")

                # Crear layout con sidebar y contenido
                page.add(
                    Row(
                        controls=[
                            # Sidebar
                            Container(
                                width=200 if sidebar_visible else 0,
                                content=Sidebar(page) if sidebar_visible else None,
                            ),
                            # Contenido principal
                            Container(
                                expand=True,
                                content=content
                            ),
                        ],
                        expand=True,
                    )
                )
            else:
                page.add(Text("Página no encontrada"))
        else:
            # Usuario no autenticado

            # Página principal con scrolling y anclajes
            content = HomeView(page, user_vm)  # Pasar user_vm a HomeView
            page.appbar = LandingNavbar(page)
            page.add(content)

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

flet.app(target=main, view="web_browser", port=8555)
