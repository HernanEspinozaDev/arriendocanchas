# views/home_view.py

from flet import Column, Container, Text, alignment
from views.who_we_are_view import WhoWeAreView
from views.services_view import ServicesView
from views.our_clients_view import OurClientsView
from views.contact_us_view import ContactUsView
from views.login_view import LoginView

def HomeView(page, user_vm):
    # Crear claves únicas para cada sección, incluyendo login
    section_ids = {
        "home": "section_home",
        "about": "section_about",
        "services": "section_services",
        "clients": "section_clients",
        "contact": "section_contact",
        "login": "section_login"
    }

    # Definir secciones, incluyendo login, con el contenido correcto para cada vista
    sections = [
        Container(
            key=section_ids["home"],
            content=Column(
                [
                    Text("Inicio", size=32, weight="bold"),
                    Text("Bienvenido a ArriendoCancha.cl", size=24),
                ],
                alignment="center"
            ),
            height=600,
            alignment=alignment.center
        ),
        Container(
            key=section_ids["about"],
            content=WhoWeAreView(),  # Llama a la vista WhoWeAreView para "Quiénes Somos"
            height=600,
            alignment=alignment.center
        ),
        Container(
            key=section_ids["services"],
            content=ServicesView(),  # Llama a la vista ServicesView para "Servicios"
            height=600,
            alignment=alignment.center
        ),
        Container(
            key=section_ids["clients"],
            content=OurClientsView(),  # Llama a la vista OurClientsView para "Nuestros Clientes"
            height=600,
            alignment=alignment.center
        ),
        Container(
            key=section_ids["contact"],
            content=ContactUsView(),  # Llama a la vista ContactUsView para "Contacto"
            height=600,
            alignment=alignment.center
        ),
        Container(
            key=section_ids["login"],
            content=LoginView(page, user_vm),  # Pasa user_vm a LoginView para "Iniciar Sesión"
            height=600,
            alignment=alignment.center
        ),
    ]

    # Crear una columna con scroll que contenga todas las secciones, incluida login
    scroll_container = Column(
        controls=sections,
        scroll="auto",  # Habilitar scroll vertical
        expand=True
    )

    # Asignar el contenedor de scroll al objeto page
    page.section_ids = section_ids
    page.scroll_container = scroll_container

    return scroll_container
