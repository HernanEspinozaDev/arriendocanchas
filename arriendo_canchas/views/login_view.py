# views/login_view.py

import flet
from flet import Column, Container, ElevatedButton, Text, TextField, alignment
from viewmodels.login_viewmodel import LoginViewModel

def LoginView(page, user_vm):
    correo_field = TextField(label="Correo Electrónico", width=300)
    contrasena_field = TextField(label="Contraseña", password=True, width=300)

    def iniciar_sesion(e):
        correo = correo_field.value
        contrasena = contrasena_field.value

        login_vm = LoginViewModel()
        user_data = login_vm.login(correo, contrasena)
        if user_data:
            if user_vm:
                user_vm.set_user(user_data)
                page.go("/dashboard")
            else:
                # Manejar caso donde user_vm no está disponible
                page.dialog = flet.AlertDialog(title=Text("Error: user_vm no está disponible"))
                page.dialog.open = True
                page.update()
        else:
            page.dialog = flet.AlertDialog(title=Text("Credenciales incorrectas"))
            page.dialog.open = True
            page.update()

    return Container(
        alignment=alignment.center,
        content=Column(
            alignment="center",
            horizontal_alignment="center",
            controls=[
                Text("Iniciar Sesión", size=32, weight="bold"),
                correo_field,
                contrasena_field,
                ElevatedButton("Iniciar Sesión", on_click=iniciar_sesion),
            ],
        ),
    )
