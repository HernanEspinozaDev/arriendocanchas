# views/widgets/navbar_pages.py

import flet
from flet import AppBar, IconButton, icons, Text

def Navbar(page, user_vm, toggle_sidebar):
    # Función para alternar el modo oscuro
    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # Función para cerrar sesión
    def logout(e):
        user_vm.logout()
        page.go("/login")

    return AppBar(
        title=Text("ArriendoCancha.cl"),
        leading=IconButton(
            icon=icons.MENU,
            on_click=toggle_sidebar  # Utiliza el callback pasado desde main.py
        ),
        actions=[
            IconButton(icon=icons.BRIGHTNESS_6, tooltip="Modo Oscuro", on_click=toggle_theme),
            IconButton(icon=icons.LOGOUT, tooltip="Cerrar Sesión", on_click=logout),
        ],
    )
