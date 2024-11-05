# arriendo_canchas/arriendo_canchas/models/cancha_model.py

import psycopg2
from services.database_service import DatabaseService

class CanchaModel:
    def __init__(self):
        self.db_service = DatabaseService()
        self.cursor = self.db_service.cursor

    def fetch_canchas(self, id_usuario):
        query = """
        SELECT c.id_cancha, c.nombre_cancha, c.tipo_cancha, co.nombre_complejo, c.id_imagen
        FROM Canchas c
        JOIN ComplejosDeportivos co ON c.id_complejo = co.id_complejo
        WHERE co.id_usuario = %s
        """
        self.cursor.execute(query, (id_usuario,))
        canchas = self.cursor.fetchall()
        return [{
            'id_cancha': c[0],
            'nombre_cancha': c[1],
            'tipo_cancha': c[2],
            'complejo_nombre': c[3],
            'id_imagen': c[4]
        } for c in canchas]

    def add_cancha(self, nombre_cancha, tipo_cancha, id_complejo, fecha_disponibilidad, id_imagen=None):
        query = """
        INSERT INTO Canchas (nombre_cancha, tipo_cancha, id_complejo, fecha_disponibilidad, id_imagen)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (nombre_cancha, tipo_cancha, id_complejo, fecha_disponibilidad, id_imagen))
        self.db_service.connection.commit()

    def update_cancha(self, id_cancha, nombre_cancha, tipo_cancha, id_complejo, fecha_disponibilidad, id_imagen=None):
        query = """
        UPDATE Canchas 
        SET nombre_cancha = %s, tipo_cancha = %s, id_complejo = %s, fecha_disponibilidad = %s, id_imagen = %s 
        WHERE id_cancha = %s
        """
        self.cursor.execute(query, (nombre_cancha, tipo_cancha, id_complejo, fecha_disponibilidad, id_imagen, id_cancha))
        self.db_service.connection.commit()

    def delete_cancha(self, id_cancha):
        query = "DELETE FROM Canchas WHERE id_cancha = %s"
        self.cursor.execute(query, (id_cancha,))
        self.db_service.connection.commit()

    def fetch_cancha_by_id(self, id_cancha):
        query = """
        SELECT c.id_cancha, c.nombre_cancha, c.tipo_cancha, co.nombre_complejo, c.id_imagen
        FROM Canchas c
        JOIN ComplejosDeportivos co ON c.id_complejo = co.id_complejo
        WHERE c.id_cancha = %s
        """
        self.cursor.execute(query, (id_cancha,))
        cancha = self.cursor.fetchone()
        if cancha:
            return {
                'id_cancha': cancha[0],
                'nombre_cancha': cancha[1],
                'tipo_cancha': cancha[2],
                'complejo_nombre': cancha[3],
                'id_imagen': cancha[4]
            }
        return None

    def close(self):
        self.db_service.close()
