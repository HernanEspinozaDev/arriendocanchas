# main.py

import flet
from flet import Page, Text, Column, Row, Container
from views.home_view import HomeView
from views.login_view import LoginView
from views.widgets.navbar import Navbar as LandingNavbar
from views.widgets.navbar_pages import Navbar as AuthenticatedNavbar
from views.widgets.sidebar import Sidebar
from viewmodels.user_viewmodel import UserViewModel

# Importar todas las vistas CRUD y adicionales
from views.authenticated.admin_view import AdminView
from views.authenticated.cliente_arrendador_view import ClienteArrendadorView
from views.authenticated.usuario_view import UsuarioView
from views.authenticated.coordinador_personal_view import CoordinadorPersonalView
from views.authenticated.empleado_atencion_view import EmpleadoAtencionView
from views.authenticated.master_admin_view import MasterAdminView
from views.authenticated.administradores_view import AdministradoresView
from views.authenticated.arrendadores_view import ArrendadoresView
from views.authenticated.coordinadores_view import CoordinadoresView
from views.authenticated.atencion_view import AtencionView
from views.authenticated.usuarios_view import UsuariosView
from views.authenticated.complejos_view import ComplejosView
from views.authenticated.canchas_view import CanchasView
from views.authenticated.mis_datos_view import MisDatosView
from views.authenticated.buscar_complejos_view import BuscarComplejosView
from views.authenticated.mis_reservas_view import MisReservasView
from views.authenticated.mis_reclamos_view import MisReclamosView

def main(page: Page):
    page.title = "ArriendoCancha.cl"
    page.theme_mode = "light"
    page.vertical_alignment = "start"

    user_vm = UserViewModel()

    page.section_ids = {
        "home": "home_section",
        "about": "about_section",
        "services": "services_section",
        "clients": "clients_section",
        "contact": "contact_section",
        "login": "login_section"
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
                # Vista principal
                if user_type == "Administrador":
                    content = AdminView(page, user_vm)
                elif user_type == "ClienteArrendador":
                    content = ClienteArrendadorView(page, user_vm)
                elif user_type == "Usuario":
                    content = UsuarioView(page, user_vm)
                elif user_type == "CoordinadorPersonal":
                    content = CoordinadorPersonalView(page, user_vm)
                elif user_type == "EmpleadoAtencion":
                    content = EmpleadoAtencionView(page, user_vm)
                elif user_type == "MasterAdmin":
                    content = MasterAdminView(page, user_vm)
                else:
                    content = Text("Tipo de usuario desconocido")
            else:
                # Manejar otras rutas
                if page.route == "/administradores":
                    content = AdministradoresView(page, user_vm)
                elif page.route == "/arrendadores":
                    content = ArrendadoresView(page, user_vm)
                elif page.route == "/coordinadores":
                    content = CoordinadoresView(page, user_vm)
                elif page.route == "/atencion":
                    content = AtencionView(page, user_vm)
                elif page.route == "/usuarios":
                    content = UsuariosView(page, user_vm)
                elif page.route == "/mis_complejos":
                    content = ComplejosView(page, user_vm)
                elif page.route == "/mis_canchas":
                    content = CanchasView(page, user_vm)
                elif page.route == "/mis_datos":
                    content = MisDatosView(page, user_vm)
                elif page.route == "/buscar_complejos":
                    content = BuscarComplejosView(page, user_vm)
                elif page.route == "/mis_reservas":
                    content = MisReservasView(page, user_vm)
                elif page.route == "/mis_reclamos":
                    content = MisReclamosView(page, user_vm)
                else:
                    content = Text("Página no encontrada")

            # Crear layout con sidebar y contenido
            page.add(
                Row(
                    controls=[
                        # Sidebar
                        Container(
                            width=200 if sidebar_visible else 0,
                            content=Sidebar(page, user_vm) if sidebar_visible else None,
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
            # Usuario no autenticado
            if page.route == "/login":
                content = LoginView(page, user_vm)
            else:
                content = HomeView(page, user_vm)
            page.appbar = LandingNavbar(page)
            page.add(content)

        page.update()

    # Función para manejar cambios en la ruta
    page.on_route_change = lambda e: route_change(page.route)

    # Establecer ruta inicial
    page.go(page.route or "/")

# Llamada a flet.app fuera de la función main
flet.app(target=main, view="web_browser", port=8555)
