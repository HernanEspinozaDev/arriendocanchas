# views/authenticated/mis_datos_view.py

from flet import (
    Column, Text, TextField, ElevatedButton, AlertDialog, TextButton
)
from models.usuario_model import UsuarioModel

def MisDatosView(page, user_vm):
    usuario_model = UsuarioModel()
    user = user_vm.get_user()
    id_usuario = user['id_usuario']
    
    # Obtener datos del usuario
    usuario = usuario_model.fetch_usuario_by_id(id_usuario)
    
    nombre_field = TextField(label="Nombre", value=usuario['nombre'])
    apellido_paterno_field = TextField(label="Apellido Paterno", value=usuario.get('apellido_paterno', ''))
    apellido_materno_field = TextField(label="Apellido Materno", value=usuario.get('apellido_materno', ''))
    telefono_field = TextField(label="Teléfono", value=usuario.get('telefono', ''))
    correo_field = TextField(label="Correo", value=usuario['correo'])
    contrasena_field = TextField(label="Nueva Contraseña", password=True)
    contrasena_confirm_field = TextField(label="Confirmar Contraseña", password=True)
    
    def actualizar_datos(e):
        nombre = nombre_field.value
        apellido_paterno = apellido_paterno_field.value
        apellido_materno = apellido_materno_field.value
        telefono = telefono_field.value
        correo = correo_field.value
        contrasena = contrasena_field.value
        contrasena_confirm = contrasena_confirm_field.value
        
        if contrasena != contrasena_confirm:
            page.dialog = AlertDialog(
                title=Text("Error"),
                content=Text("Las contraseñas no coinciden"),
                actions=[
                    TextButton("OK", on_click=lambda e: setattr(page.dialog, 'open', False)),
                ],
            )
            page.dialog.open = True
            page.update()
            return
        
        try:
            usuario_model.update_usuario_full(
                id_usuario=id_usuario,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                telefono=telefono,
                correo=correo,
                contrasena=contrasena if contrasena else None
            )
            page.dialog = AlertDialog(
                title=Text("Datos Actualizados"),
                content=Text("Sus datos han sido actualizados exitosamente"),
                actions=[
                    TextButton("OK", on_click=lambda e: setattr(page.dialog, 'open', False)),
                ],
            )
            page.dialog.open = True
            page.update()
        except Exception as ex:
            print(f"Error al actualizar datos: {ex}")
            page.dialog = AlertDialog(
                title=Text("Error"),
                content=Text("No se pudo actualizar sus datos. Por favor, inténtelo de nuevo."),
                actions=[
                    TextButton("OK", on_click=lambda e: setattr(page.dialog, 'open', False)),
                ],
            )
            page.dialog.open = True
            page.update()
    
    return Column(
        [
            Text("Mis Datos", size=24, weight="bold"),
            nombre_field,
            apellido_paterno_field,
            apellido_materno_field,
            telefono_field,
            correo_field,
            contrasena_field,
            contrasena_confirm_field,
            ElevatedButton("Actualizar Datos", on_click=actualizar_datos),
        ]
    )
