from neo4j import GraphDatabase


class BaseDatosNeo4j:

    def __init__(self, uri, usuario, password):

        self.driver = GraphDatabase.driver(
            uri,
            auth=(usuario, password)
        )

    def cerrar(self):

        self.driver.close()

    def insertar_jugador(self, jugador):
        #Inserta un jugador y sus relaciones dentro del grafo Neo4j.


        query = """

        MERGE (j:Jugador {id: $id})

        SET j.nombre = $nombre,
            j.edad = $edad,
            j.overall = $overall,
            j.potencial = $potencial,
            j.ritmo = $ritmo,
            j.tiro = $tiro,
            j.pase = $pase,
            j.regate = $regate,
            j.defensa = $defensa,
            j.fisico = $fisico,
            j.valor = $valor,
            j.salario = $salario

        MERGE (e:Equipo {nombre: $equipo})
        MERGE (p:Posicion {nombre: $posicion})
        MERGE (l:Liga {nombre: $liga})

        MERGE (j)-[:JUEGA_EN]->(e)
        MERGE (j)-[:OCUPA]->(p)
        MERGE (e)-[:PERTENECE_A]->(l)

        """

        with self.driver.session() as session:

            session.run(

                query,

                id=jugador.id,
                nombre=jugador.nombre,

                edad=jugador.edad,
                posicion=jugador.posicion,
                equipo=jugador.equipo,
                liga=jugador.liga,

                overall=jugador.overall,
                potencial=jugador.potencial,

                ritmo=jugador.ritmo,
                tiro=jugador.tiro,
                pase=jugador.pase,
                regate=jugador.regate,
                defensa=jugador.defensa,
                fisico=jugador.fisico,

                valor=jugador.valor,
                salario=jugador.salario
            )

    def insertar_multiples_jugadores(self, jugadores):
        #Inserta una lista de jugadores.

        for jugador in jugadores:

            self.insertar_jugador(jugador)