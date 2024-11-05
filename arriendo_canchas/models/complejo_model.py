# arriendo_canchas/arriendo_canchas/models/complejo_model.py

import psycopg2
from services.database_service import DatabaseService

class ComplejoModel:
    def __init__(self):
        self.db_service = DatabaseService()
        self.cursor = self.db_service.cursor

    def fetch_complejos(self, id_usuario):
        query = """
        SELECT id_complejo, nombre_complejo, direccion, id_imagen 
        FROM ComplejosDeportivos 
        WHERE id_usuario = %s
        """
        self.cursor.execute(query, (id_usuario,))
        complejos = self.cursor.fetchall()
        return [{
            'id_complejo': c[0],
            'nombre_complejo': c[1],
            'direccion': c[2],
            'id_imagen': c[3]
        } for c in complejos]

    def add_complejo(self, nombre_complejo, direccion, id_usuario, telefono=None, correo=None, id_imagen=None, cantidad_canchas=0):
        query = """
        INSERT INTO ComplejosDeportivos (nombre_complejo, direccion, id_usuario, telefono, correo, id_imagen, cantidad_canchas)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (nombre_complejo, direccion, id_usuario, telefono, correo, id_imagen, cantidad_canchas))
        self.db_service.connection.commit()

    def update_complejo(self, id_complejo, nombre_complejo, direccion, id_imagen=None):
        query = """
        UPDATE ComplejosDeportivos 
        SET nombre_complejo = %s, direccion = %s, id_imagen = %s 
        WHERE id_complejo = %s
        """
        self.cursor.execute(query, (nombre_complejo, direccion, id_imagen, id_complejo))
        self.db_service.connection.commit()

    def delete_complejo(self, id_complejo):
        query = "DELETE FROM ComplejosDeportivos WHERE id_complejo = %s"
        self.cursor.execute(query, (id_complejo,))
        self.db_service.connection.commit()

    def fetch_complejo_by_id(self, id_complejo):
        query = """
        SELECT id_complejo, nombre_complejo, direccion, id_imagen 
        FROM ComplejosDeportivos 
        WHERE id_complejo = %s
        """
        self.cursor.execute(query, (id_complejo,))
        complejo = self.cursor.fetchone()
        if complejo:
            return {
                'id_complejo': complejo[0],
                'nombre_complejo': complejo[1],
                'direccion': complejo[2],
                'id_imagen': complejo[3]
            }
        return None

    def close(self):
        self.db_service.close()
