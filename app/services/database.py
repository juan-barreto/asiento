import sqlite3
import datetime


class Database:

    def __init__(self):

        self._create_tables()

    def _connect(self):

        return sqlite3.connect("historial.db")

    def _create_tables(self):

        with self._connect() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversiones (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    fecha_procesado TEXT NOT NULL,

                    fecha_extracto_inicial TEXT NOT NULL,

                    fecha_extracto_final TEXT NOT NULL,

                    nombre_archivo TEXT NOT NULL,

                    banco TEXT NOT NULL,

                    total_movimientos INTEGER NOT NULL,

                    total_seguros INTEGER NOT NULL,

                    total_revisar INTEGER NOT NULL,

                    resultado_json TEXT NOT NULL

                )
            """)

    def save_result(self, resultado, nombre_archivo):

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
                    banco,
                    total_movimientos,
                    total_seguros,
                    total_revisar,
                    resultado_json

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

            """,
            (
                fecha,
                resultado.movimientos[0].fecha,
                resultado.movimientos[-1].fecha,
                nombre_archivo,
                resultado.banco,
                resultado.stats.total_movimientos,
                resultado.stats.total_seguros,
                resultado.stats.total_revisar,
                resultado.model_dump_json()
            )
            )

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
                "archivo": fila[4],
                "banco": fila[5],
                "movimientos": fila[6],
                "seguros": fila[7],
                "revisar": fila[8]

            }

            resultados.append(resultado)

        return resultados

if __name__ == "__main__":

    from pathlib import Path
    from app.services.pipeline import procesar_extracto

    pdf_path = r"C:\Users\Juan\Desktop\ASIENTO\app\services\Extracto_Cuentas_Galicia_2026_01_30.pdf"

    resultado = procesar_extracto(pdf_path)

    database = Database()

    database.save_result(
        resultado,
        Path(pdf_path).name
    )

    resultados = database.get_results()

    for fila in resultados:
        print(fila)

