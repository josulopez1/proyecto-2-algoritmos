from neo4j_driver import Neo4jManager

neo = Neo4jManager()

print(neo.probar_conexion())

neo.cerrar()
