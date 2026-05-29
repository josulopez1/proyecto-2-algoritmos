from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import numpy as np


class SimilitudCoseno:

    def __init__(self, jugadores):

        self.jugadores = jugadores

        # Crear matriz de vectores
        matriz = np.array([

            jugador.obtener_vector()

            for jugador in self.jugadores
        ])

        # Normalizar atributos
        scaler = MinMaxScaler()

        self.matriz_normalizada = scaler.fit_transform(
            matriz
        )

    def encontrar_similares(
        self,
        nombre_jugador,
        top_n=5
    ):
        indice_objetivo = None

        # Buscar jugador objetivo
        for i, jugador in enumerate(self.jugadores):

            if jugador.nombre.lower() == nombre_jugador.lower():

                indice_objetivo = i
                break

        if indice_objetivo is None:

            raise ValueError(
                "Jugador no encontrado"
            )

        # Vector objetivo
        vector_objetivo = self.matriz_normalizada[
            indice_objetivo
        ]

        # Calcular similitudes
        similitudes = cosine_similarity(

            [vector_objetivo],
            self.matriz_normalizada

        )[0]

        resultados = []

        for i, score in enumerate(similitudes):

            if i != indice_objetivo:

                resultados.append({

                    "jugador": self.jugadores[i],

                    "similitud": round(score, 4)
                })

        # Ordenar descendente
        resultados.sort(

            key=lambda x: x["similitud"],

            reverse=True
        )

        return resultados[:top_n]