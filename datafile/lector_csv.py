import pandas as pd
from jugador import Jugador


class LectorCSV:

    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv

    def cargar_jugadores(self):

        df = pd.read_csv(
            self.ruta_csv,
            sep=";",
            encoding="utf-8"
        )

        jugadores = []

        for indice, row in df.iterrows():

            nombre = row.get("name")
            if pd.isna(nombre):
                nombre = f"Jugador_{indice}"

            equipo = row.get("team")
            if pd.isna(equipo):
                equipo = "Sin Equipo"

            pais = row.get("country")
            if pd.isna(pais):
                pais = "Desconocida"

            posicion = row.get("best_position")
            if pd.isna(posicion):
                posicion = "Desconocida"

            data = {

                # Identificación
                "id": int(indice),
                "nombre": str(nombre),

                # Información general
                "edad": int(row.get("age", 0))
                if pd.notna(row.get("age"))
                else 0,

                "posicion": str(posicion),
                "equipo": str(equipo),
                "liga": str(pais),

                # Ratings FIFA
                "overall": int(row.get("best_overall_rating", 0))
                if pd.notna(row.get("best_overall_rating"))
                else 0,

                "potencial": int(row.get("best_overall_rating", 0))
                if pd.notna(row.get("best_overall_rating"))
                else 0,

                # Estadísticas principales
                "ritmo": int(row.get("sprint_speed", 0))
                if pd.notna(row.get("sprint_speed"))
                else 0,

                "tiro": int(row.get("finishing", 0))
                if pd.notna(row.get("finishing"))
                else 0,

                "pase": int(row.get("short_passing", 0))
                if pd.notna(row.get("short_passing"))
                else 0,

                "regate": int(row.get("dribbling", 0))
                if pd.notna(row.get("dribbling"))
                else 0,

                "defensa": int(row.get("defensive_awareness", 0))
                if pd.notna(row.get("defensive_awareness"))
                else 0,

                "fisico": int(row.get("strength", 0))
                if pd.notna(row.get("strength"))
                else 0,

                # Economía
                "valor": 0,
                "salario": 0
            }

            jugadores.append(Jugador(data))

        return jugadores