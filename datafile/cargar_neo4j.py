import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from lector_csv import LectorCSV
from base_datos import BaseDatosNeo4j

lector = LectorCSV(
    "datafile/dataplayers.csv"
)

jugadores = lector.cargar_jugadores()

print(f"Jugadores encontrados: {len(jugadores)}")

db = BaseDatosNeo4j(
    "neo4j://127.0.0.1:7687",
    "neo4j",
    "12345678"
)

db.insertar_multiples_jugadores(jugadores)

db.cerrar()

print(
    f"Se insertaron {len(jugadores)} jugadores correctamente."
)