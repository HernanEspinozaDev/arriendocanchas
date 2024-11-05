# views/widgets/sidebar.py

from flet import Column, ListTile, Icon, icons, Text

def Sidebar(page, user_vm):
    def navigate_to(route):
        page.go(route)
        page.update()

    user = user_vm.get_user()
    user_type = user['tipo_cuenta']

    controls = []

    # Común para todos los usuarios
    controls.append(
        ListTile(
            leading=Icon(icons.HOME),
            title=Text("Inicio"),
            on_click=lambda e: navigate_to("/dashboard"),
        )
    )

    # Elementos basados en el tipo de usuario
    if user_type == "MasterAdmin":
        controls.extend([
            ListTile(
                leading=Icon(icons.PEOPLE),
                title=Text("Administradores"),
                on_click=lambda e: navigate_to("/administradores"),
            ),
            ListTile(
                leading=Icon(icons.PEOPLE_OUTLINE),
                title=Text("Arrendadores"),
                on_click=lambda e: navigate_to("/arrendadores"),
            ),
            ListTile(
                leading=Icon(icons.SUPERVISOR_ACCOUNT),
                title=Text("Coordinadores"),
                on_click=lambda e: navigate_to("/coordinadores"),
            ),
            ListTile(
                leading=Icon(icons.SUPPORT_AGENT),
                title=Text("Atención"),
                on_click=lambda e: navigate_to("/atencion"),
            ),
            ListTile(
                leading=Icon(icons.GROUP),
                title=Text("Usuarios"),
                on_click=lambda e: navigate_to("/usuarios"),
            ),
        ])
    elif user_type == "Administrador":
        controls.extend([
            ListTile(
                leading=Icon(icons.PEOPLE_OUTLINE),
                title=Text("Arrendadores"),
                on_click=lambda e: navigate_to("/arrendadores"),
            ),
            ListTile(
                leading=Icon(icons.SUPERVISOR_ACCOUNT),
                title=Text("Coordinadores"),
                on_click=lambda e: navigate_to("/coordinadores"),
            ),
            ListTile(
                leading=Icon(icons.SUPPORT_AGENT),
                title=Text("Atención"),
                on_click=lambda e: navigate_to("/atencion"),
            ),
            ListTile(
                leading=Icon(icons.GROUP),
                title=Text("Usuarios"),
                on_click=lambda e: navigate_to("/usuarios"),
            ),
        ])
    elif user_type == "ClienteArrendador":
        controls.extend([
            ListTile(
                leading=Icon(icons.BUSINESS),
                title=Text("Mis Complejos"),
                on_click=lambda e: navigate_to("/mis_complejos"),
            ),
            ListTile(
                leading=Icon(icons.SPORTS_SOCCER),
                title=Text("Mis Canchas"),
                on_click=lambda e: navigate_to("/mis_canchas"),
            ),
            ListTile(
                leading=Icon(icons.SUPERVISOR_ACCOUNT),
                title=Text("Mis Coordinadores"),
                on_click=lambda e: navigate_to("/mis_coordinadores"),
            ),
            ListTile(
                leading=Icon(icons.SUPPORT_AGENT),
                title=Text("Mis Empleados de Atención"),
                on_click=lambda e: navigate_to("/mis_empleados_atencion"),
            ),
            ListTile(
                leading=Icon(icons.GROUP),
                title=Text("Usuarios"),
                on_click=lambda e: navigate_to("/usuarios"),
            ),
        ])
    elif user_type == "Usuario":
        controls.extend([
            ListTile(
                leading=Icon(icons.ACCOUNT_BOX),
                title=Text("Mis Datos"),
                on_click=lambda e: navigate_to("/mis_datos"),
            ),
            ListTile(
                leading=Icon(icons.SEARCH),
                title=Text("Buscar Complejos"),
                on_click=lambda e: navigate_to("/buscar_complejos"),
            ),
            ListTile(
                leading=Icon(icons.BOOKMARK),
                title=Text("Mis Reservas"),
                on_click=lambda e: navigate_to("/mis_reservas"),
            ),
            ListTile(
                leading=Icon(icons.REPORT),
                title=Text("Mis Reclamos"),
                on_click=lambda e: navigate_to("/mis_reclamos"),
            ),
        ])
    else:
        # Otros tipos de usuario
        pass

    return Column(
        controls=controls
    )
