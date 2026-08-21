import sqlite3
import datetime
from pathlib import Path
import os

class Database:

    def __init__(self):

        self._create_table_conversiones()
        self._create_table_templates()

    def _database_path(self) -> Path:

        appdata = Path(
            os.getenv("LOCALAPPDATA")
        )

        carpeta = appdata / "Asiento"

        carpeta.mkdir(exist_ok = True
        )
        return carpeta / "historial.db"

    def _connect(self):

        return sqlite3.connect(self._database_path())

    
    def _create_table_templates(self):

        with self._connect() as connection:

            cursor = connection.cursor()

            cursor.execute("""

                CREATE TABLE IF NOT EXISTS templates(
                
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    nombre TEXT NOT NULL,
                    
                    config_json TEXT NOT NULL
                )
                """)

    def save_new_template(self, config):

        if not config:
            raise ValueError(
                "No hay plantilla para guardar"
            )
        
        with self._connect() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO templates(

                    nombre,
                    config_json
                )

                VALUES (?, ?)


                    """,
                    (
                        config.name,
                        config.model_dump_json()
                    ))

    def get_templates(self):
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, nombre, config_json FROM templates")
            return cursor.fetchall()

    def _create_table_conversiones(self):

        with self._connect() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversiones (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    fecha_procesado TEXT NOT NULL,

                    fecha_extracto_inicial TEXT NOT NULL,

                    fecha_extracto_final TEXT NOT NULL,

                    nombre_archivo TEXT NOT NULL,

                    ruta_archivo TEXT NOT NULL,

                    banco TEXT NOT NULL,

                    total_movimientos INTEGER NOT NULL,

                    total_seguros INTEGER NOT NULL,

                    total_revisar INTEGER NOT NULL,

                    resultado_json TEXT NOT NULL

                )
            """)

    def save_result(self, resultado, nombre_archivo, ruta_archivo):

        if not resultado.movimientos:
            raise ValueError(
                "No se puede guardar un resultado sin movimientos"
            )

        fecha = datetime.datetime.now().isoformat()

        with self._connect() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO conversiones(

                    fecha_procesado,
                    fecha_extracto_inicial,
                    fecha_extracto_final,
                    nombre_archivo,
                    ruta_archivo,
                    banco,
                    total_movimientos,
                    total_seguros,
                    total_revisar,
                    resultado_json

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            """,
            (
                fecha,
                resultado.movimientos[0].fecha,
                resultado.movimientos[-1].fecha,
                nombre_archivo,
                ruta_archivo,
                resultado.banco,
                resultado.stats.total_movimientos,
                resultado.stats.total_seguros,
                resultado.stats.total_revisar,
                resultado.model_dump_json()
            )
            )
            return cursor.lastrowid
    def get_results(self):

        with self._connect() as connection:

            cursor = connection.cursor()

            cursor.execute("""
            SELECT

                id,
                fecha_procesado,
                fecha_extracto_inicial,
                fecha_extracto_final,
                nombre_archivo,
                ruta_archivo,
                banco,
                total_movimientos,
                total_seguros,
                total_revisar

            FROM conversiones

            ORDER BY fecha_procesado DESC
                    """)

            filas = cursor.fetchall()

        resultados = []

        for fila in filas:
            resultado = {

                "id": fila[0],
                "fecha": fila[1],
                "fecha_inicial": fila[2],
                "fecha_final": fila[3],
                "nombre_archivo": fila[4],
                "ruta_archivo": fila[5],
                "banco": fila[6],
                "movimientos": fila[7],
                "seguros": fila[8],
                "revisar": fila[9]

            }

            resultados.append(resultado)

        return resultados

    def get_pdf_path(self, conversion_id):
    
            with self._connect() as connection:
    
                cursor = connection.cursor()
    
                cursor.execute("""
                SELECT
    
                    ruta_archivo
    
                FROM conversiones
    
                WHERE id = ?
                        """,
                (conversion_id,)
                        )

                fila = cursor.fetchone()
    
    
            if fila is None:
                return None

            return fila[0]

    def update_result(self, conversion_id: int, resultado):

        with self._connect() as connection:

            cursor = connection.cursor()
            print("ID:", conversion_id)

            cursor.execute(
                """
                UPDATE conversiones
                SET
                    total_seguros = ?,
                    total_revisar = ?,
                    resultado_json = ?
                WHERE id = ?
                """,
                (
                    resultado.stats.total_seguros,
                    resultado.stats.total_revisar,
                    resultado.model_dump_json(),
                    conversion_id
                )
            )

            print("Filas modificadas:", cursor.rowcount)
            print("UPDATE EJECUTADO")

    def delete_result(self, conversion_id: int):

        with self._connect() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM conversiones
                WHERE id = ?

            """, (conversion_id,))

            connection.commit()

            return cursor.rowcount
    def get_result_json(self, conversion_id: int) -> str | None:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT resultado_json FROM conversiones WHERE id = ?", (conversion_id,))
            fila = cursor.fetchone()
        return fila[0] if fila else None

    def get_conversion(self, conversion_id):
        with self._connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    nombre_archivo,
                    ruta_archivo,
                    banco,
                    total_movimientos,
                    total_seguros,
                    total_revisar
                FROM conversiones
                WHERE id = ?
            """, (conversion_id,))

            fila = cursor.fetchone()

        return fila


if __name__ == "__main__":

    from pathlib import Path
    from app.services.pipeline import procesar_extracto

    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"

    resultado = procesar_extracto(pdf_path)

    database = Database()

    database.save_result(
        resultado,
        Path(pdf_path).name,
        pdf_path
    )

    resultados = database.get_results()

    for fila in resultados:
        print(fila)

