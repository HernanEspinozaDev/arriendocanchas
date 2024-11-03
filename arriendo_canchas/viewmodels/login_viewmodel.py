# viewmodels/login_viewmodel.py

from services.database_service import DatabaseService

class LoginViewModel:
    def __init__(self):
        pass

    def login(self, correo, contrasena):
        db_service = DatabaseService()
        try:
            query = """
            SELECT id_usuario, nombre, tipo_cuenta, contrasena
            FROM usuarios
            WHERE correo = %s
            """
            db_service.cursor.execute(query, (correo,))
            user = db_service.cursor.fetchone()
            if user:
                user_id, nombre, tipo_cuenta, hashed_password = user
                # Verificar la contraseña
                verify_query = "SELECT crypt(%s, %s) = %s AS password_match"
                db_service.cursor.execute(verify_query, (contrasena, hashed_password, hashed_password))
                result = db_service.cursor.fetchone()
                if result and result[0]:
                    # Devolver los datos del usuario
                    user_data = {
                        'id_usuario': user_id,
                        'nombre': nombre,
                        'tipo_cuenta': tipo_cuenta,
                        'correo': correo,
                    }
                    return user_data
            return None
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return None
        finally:
            db_service.close()
