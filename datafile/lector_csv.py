import pandas as pd
from jugador import Jugador


class LectorCSV:

    def __init__(self, ruta_csv):

        self.ruta_csv = ruta_csv

    def cargar_jugadores(self):
        #Lee el CSV y convierte cada fila en un objeto Jugador.

        df = pd.read_csv(self.ruta_csv)

        jugadores = []

        for _, row in df.iterrows():

            data = {

                # Identificación
                "id": row.get("sofifa_id"),
                "nombre": row.get("short_name"),

                # Información general
                "edad": row.get("age"),
                "posicion": row.get("player_positions"),
                "equipo": row.get("club_name"),
                "liga": row.get("league_name"),

                # Ratings FIFA
                "overall": row.get("overall"),
                "potencial": row.get("potential"),

                # Estadísticas principales
                "ritmo": row.get("pace"),
                "tiro": row.get("shooting"),
                "pase": row.get("passing"),
                "regate": row.get("dribbling"),
                "defensa": row.get("defending"),
                "fisico": row.get("physic"),

                # Economía
                "valor": row.get("value_eur"),
                "salario": row.get("wage_eur")
            }

            jugador = Jugador(data)

            jugadores.append(jugador)

        return jugadores