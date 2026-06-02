from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USUARIO = "neo4j"
PASSWORD = "12345678"  # cambia por la tuya


class Neo4jManager:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            URI,
            auth=(USUARIO, PASSWORD)
        )

    def cerrar(self):
        self.driver.close()

    def obtener_pagerank(self):

        query = """
        CALL gds.pageRank.stream('jugadoresGraph')
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).nombre AS jugador, score
        ORDER BY score DESC
        """

        with self.driver.session() as session:

            resultado = session.run(query)

            jugadores = {}

            for row in resultado:
                jugadores[row["jugador"]] = row["score"]

            return jugadores
