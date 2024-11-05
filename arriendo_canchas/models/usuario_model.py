# arriendo_canchas/arriendo_canchas/models/usuario_model.py

import psycopg2
from services.database_service import DatabaseService

class UsuarioModel:
    def __init__(self):
        self.db_service = DatabaseService()
        self.cursor = self.db_service.cursor

    def fetch_usuarios(self, tipo_cuenta='Usuario'):
        query = """
        SELECT id_usuario, nombre, correo 
        FROM Usuarios 
        WHERE tipo_cuenta = %s
        """
        self.cursor.execute(query, (tipo_cuenta,))
        usuarios = self.cursor.fetchall()
        return [{'id_usuario': u[0], 'nombre': u[1], 'correo': u[2]} for u in usuarios]

    def add_usuario(self, rut, nombre, apellido_paterno, apellido_materno, telefono, correo, contrasena, tipo_cuenta, id_admin_responsable=None):
        query = """
        INSERT INTO Usuarios (rut, nombre, apellido_paterno, apellido_materno, telefono, correo, contrasena, tipo_cuenta, id_admin_responsable)
        VALUES (%s, %s, %s, %s, %s, %s, crypt(%s, gen_salt('bf')), %s, %s)
        """
        self.cursor.execute(query, (rut, nombre, apellido_paterno, apellido_materno, telefono, correo, contrasena, tipo_cuenta, id_admin_responsable))
        self.db_service.connection.commit()

    def update_usuario(self, id_usuario, nombre, correo):
        query = """
        UPDATE Usuarios 
        SET nombre = %s, correo = %s 
        WHERE id_usuario = %s
        """
        self.cursor.execute(query, (nombre, correo, id_usuario))
        self.db_service.connection.commit()

    def delete_usuario(self, id_usuario):
        query = "DELETE FROM Usuarios WHERE id_usuario = %s"
        self.cursor.execute(query, (id_usuario,))
        self.db_service.connection.commit()

    def fetch_usuario_by_id(self, id_usuario):
        query = """
        SELECT id_usuario, nombre, correo 
        FROM Usuarios 
        WHERE id_usuario = %s
        """
        self.cursor.execute(query, (id_usuario,))
        usuario = self.cursor.fetchone()
        if usuario:
            return {'id_usuario': usuario[0], 'nombre': usuario[1], 'correo': usuario[2]}
        return None

    def close(self):
        self.db_service.close()
