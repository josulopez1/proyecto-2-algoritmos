import pandas as pd

class Jugador:

    def __init__(self, datos):

        # Guardamos TODOS los datos del CSV
        self.datos = datos

        # Algunos atributos importantes
        self.nombre = datos.get("name")
        self.edad = datos.get("age")
        self.media = datos.get("best_overall_rating")
        self.posicion = datos.get("best_position")
        self.club = datos.get("club_name")
        self.precio = datos.get("precio_aproximado")

    def __str__(self):

        return f"{self.nombre} ({self.media})"


class Database:

    def __init__(self, archivo_csv):

        # Guardamos el nombre/ruta del archivo
        self.archivo_csv = archivo_csv

        # Lista donde estarán todos los jugadores
        self.jugadores = []

        # Cargar automáticamente el CSV
        self.cargar_datos()

    def cargar_datos(self):

        # Leer CSV con pandas
        df = pd.read_csv(self.archivo_csv, sep=';')

        # Recorrer cada fila del CSV
        for _, fila in df.iterrows():

            # Convertir fila a diccionario
            datos_jugador = fila.to_dict()

            # Crear objeto Jugador
            jugador = Jugador(datos_jugador)

            # Guardarlo en la lista
            self.jugadores.append(jugador)