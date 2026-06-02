# Tactical Graph Scouting

Sistema de recomendación de jugadores de fútbol basado en algoritmos de similitud y bases de datos orientadas a grafos.

## Integrantes

* Julio Fernando Ortiz Alvarado – 251190
* Juan José Mazariegos Cuevas – 25128
* José Carlos Gonzáles Argueta – 25652
* Josué Sebastián López Velásquez – 25715



# Descripción del proyecto

Tactical Graph Scouting es un sistema de recomendación diseñado para ayudar a entrenadores, scouts y directores deportivos a encontrar jugadores con perfiles similares a un jugador objetivo.

El sistema combina diferentes enfoques de recomendación:

* Similitud de Coseno
* Coeficiente de Jaccard
* PageRank sobre una base de datos Neo4j
* Modelado de relaciones mediante grafos

La meta es reducir la incertidumbre en procesos de scouting y fichajes mediante recomendaciones basadas en datos reales.



# Tecnologías utilizadas

* Python 3.11+
* CustomTkinter
* Pandas
* NumPy
* Scikit-Learn
* Neo4j
* Cypher



# Estructura del proyecto

```text
proyecto-2-algoritmos/

│
├── BusquedaDeJugadores.py
├── jugador.py
├── lectorcsv.py
├── similitud_coseno.py
├── base_datos.py
│
├── datafile/
│   ├── dataplayers.csv
│   ├── init.cypher
│   └── pagerank.cypher
│
└── README.md
```

# Algoritmos implementados

## 1. Similitud de Coseno

Utilizada para comparar el rendimiento cuantitativo de los jugadores mediante vectores estadísticos normalizados.

Se consideran atributos como:

* Ritmo
* Tiro
* Pase
* Regate
* Defensa
* Físico



## 2. Coeficiente de Jaccard

Utilizado para comparar características cualitativas de los jugadores.

Ejemplos:

* Regateador
* Veloz
* Creativo
* Goleador



## 3. PageRank

Implementado sobre Neo4j para medir la relevancia de un jugador dentro de una red de relaciones.

Las relaciones consideradas incluyen:

* Jugador → Equipo
* Jugador → Posición
* Jugador → Liga



# Base de datos

La información utilizada proviene de un conjunto de datos real de jugadores de fútbol.

La base de datos en Neo4j está compuesta por:

## Nodos

* Jugador
* Equipo
* Posición
* Liga

## Relaciones

* JUEGA_EN
* OCUPA
* PERTENECE_A



# Instalación

## 1. Clonar repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
```

## 2. Instalar dependencias

```bash
pip install customtkinter
pip install pandas
pip install numpy
pip install scikit-learn
pip install neo4j
```

## 3. Configurar Neo4j

Instalar Neo4j Desktop.

Crear una base de datos local.

Ejecutar los scripts:

```text
init.cypher
pagerank.cypher
```

para generar la estructura del grafo.

## 4. Ejecutar el programa

```bash
python BusquedaDeJugadores.py
```



# Uso del sistema

1. Ejecutar la aplicación.
2. Seleccionar un jugador del menú desplegable.
3. Presionar "Ejecutar Análisis Híbrido".
4. Revisar los resultados obtenidos mediante:

   * Similitud de Jaccard
   * Similitud de Coseno
   * PageRank



# Dataset

El sistema utiliza información real de jugadores profesionales almacenada en:

```text
datafile/dataplayers.csv
```

# Conclusión

Tactical Graph Scouting demuestra cómo los algoritmos de recomendación y las bases de datos orientadas a grafos pueden utilizarse para apoyar procesos de scouting deportivo, proporcionando recomendaciones más consistentes, objetivas y contextualizadas.
