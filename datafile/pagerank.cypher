CALL gds.graph.project(
    'jugadoresGraph',
    ['Jugador', 'Equipo', 'Atributo'],
    ['JUEGA_EN', 'DESTACA_EN']
);

CALL gds.pageRank.stream('jugadoresGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).nombre AS jugador, score
ORDER BY score DESC;
