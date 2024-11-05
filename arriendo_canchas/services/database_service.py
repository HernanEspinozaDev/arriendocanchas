# services/database_service.py

import psycopg2

class DatabaseService:
    def __init__(self):
        # Conexión a la base de datos PostgreSQL en Amazon RDS
        self.connection = psycopg2.connect(
            host='arriendocanchasdb.cvqy64y6ixpr.us-east-1.rds.amazonaws.com',
            database='postgres',
            user='postgres',
            password='aRRCANCHAS24',
            port='5432'
        )
        self.cursor = self.connection.cursor()
        # Establecer el search_path al esquema correcto
        try:
            self.cursor.execute("SET search_path TO arrcanchasdb")
            self.connection.commit()
            print("search_path establecido a 'arriendocanchasdb'")
        except Exception as e:
            print(f"Error al establecer search_path: {e}")
            self.close()
            raise e

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
