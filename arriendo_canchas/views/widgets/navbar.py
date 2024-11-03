# views/widgets/navbar.py

from flet import AppBar, IconButton, icons, Text

def Navbar(page):
    # Función para navegar a una sección específica
    def scroll_to_section(section_key):
        def scroll_to(e):
            page.scroll_container.scroll_to(key=section_key, duration=500)
            page.update()
        return scroll_to

    return AppBar(
        title=Text("ArriendoCancha.cl"),
        actions=[
            IconButton(icon=icons.HOME, tooltip="Inicio", on_click=scroll_to_section(page.section_ids["home"])),
            IconButton(icon=icons.INFO, tooltip="Quiénes Somos", on_click=scroll_to_section(page.section_ids["about"])),
            IconButton(icon=icons.MISCELLANEOUS_SERVICES, tooltip="Servicios", on_click=scroll_to_section(page.section_ids["services"])),
            IconButton(icon=icons.PEOPLE, tooltip="Clientes", on_click=scroll_to_section(page.section_ids["clients"])),
            IconButton(icon=icons.CONTACT_PAGE, tooltip="Contacto", on_click=scroll_to_section(page.section_ids["contact"])),
            IconButton(icon=icons.ACCOUNT_CIRCLE, tooltip="Iniciar Sesión", on_click=scroll_to_section(page.section_ids["login"])),  # Navegar a login
        ],
    )
