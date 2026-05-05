// Crear nodos
MERGE (p1:Jugador {nombre: "Lamine Yamal"})
SET p1.edad = 16, p1.valor_mercado = 90, p1.media = 85

MERGE (p2:Jugador {nombre: "Jamal Musiala"})
SET p2.edad = 21, p2.valor_mercado = 110, p2.media = 88

MERGE (eq:Equipo {nombre: "FC Barcelona"})
SET eq.presupuesto = 800

MERGE (pos:Posicion {sigla: "MCO"})

MERGE (vel:Atributo {tipo: "Velocidad"})
MERGE (reg:Atributo {tipo: "Regate"})

// Crear relaciones
MERGE (p1)-[:JUEGA_EN]->(eq)
MERGE (p2)-[:JUEGA_EN]->(eq)

MERGE (p1)-[:TIENE_POSICION]->(pos)
MERGE (p2)-[:TIENE_POSICION]->(pos)

MERGE (p1)-[:DESTACA_EN]->(vel)
MERGE (p1)-[:DESTACA_EN]->(reg)

MERGE (p2)-[:DESTACA_EN]->(vel)
MERGE (p2)-[:DESTACA_EN]->(reg)
