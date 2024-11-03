# views/widgets/sidebar.py

from flet import Column, ListTile, Icon, icons, Text

def Sidebar(page):
    def navigate_to(route):
        page.go(route)
        page.update()

    return Column(
        controls=[
            ListTile(
                leading=Icon(icons.HOME),
                title=Text("Inicio"),
                on_click=lambda e: navigate_to("/dashboard"),
            ),
            # Añade más opciones aquí
        ]
    )
