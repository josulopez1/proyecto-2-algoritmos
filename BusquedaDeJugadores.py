import os
import tkinter as messagebox
import customtkinter as ctk
import numpy as np
import pandas as pd
from neo4j import GraphDatabase
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# 1. MODELO DE DATOS RESILIENTE (JUGADOR)
class Jugador:
    def __init__(self, datos):
        # Guardamos el diccionario completo para no perder ninguna columna del CSV original
        self.datos = datos

        # Mapeo idéntico al Lector, soportando ambas nomenclaturas por seguridad
        self.id = datos.get("id")
        self.nombre = datos.get("nombre") if datos.get("nombre") else datos.get("name")
        self.edad = datos.get("edad") if datos.get("edad") else datos.get("age", 0)
        
        # Soporte para la columna de equipo y liga del CSV de la Fase 2
        self.equipo = datos.get("equipo") if datos.get("equipo") else datos.get("club_name", "Sin Equipo")
        if self.equipo == "Sin Equipo" and datos.get("team"):
            self.equipo = datos.get("team")
            
        self.liga = datos.get("liga") if datos.get("liga") else datos.get("country", "Desconocida")
        self.posicion = datos.get("posicion") if datos.get("posicion") else datos.get("best_position", "Desconocida")

        # Ratings de Rendimiento Técnico (FIFA / EA Sports Stats)
        self.overall = datos.get("overall") if datos.get("overall") else datos.get("best_overall_rating", 0)
        self.potencial = datos.get("potencial") if datos.get("potencial") else datos.get("best_overall_rating", 0)
        
        # Mapeo de métricas físicas cuantitativas para la matriz de Coseno
        self.ritmo = datos.get("ritmo") if datos.get("ritmo") else datos.get("sprint_speed", 0)
        self.tiro = datos.get("tiro") if datos.get("tiro") else datos.get("finishing", 0)
        self.pase = datos.get("pase") if datos.get("pase") else datos.get("short_passing", 0)
        self.regate = datos.get("regate") if datos.get("regate") else datos.get("dribbling", 0)
        self.defensa = datos.get("defensa") if datos.get("defensa") else datos.get("defensive_awareness", 0)
        self.fisico = datos.get("fisico") if datos.get("fisico") else datos.get("strength", 0)

        # Variables económicas solicitadas en la rúbrica de administración
        self.valor = datos.get("valor") if datos.get("valor") else datos.get("precio_aproximado", 0)
        self.salario = datos.get("salario", 0)

        # LÓGICA DE JACCARD (Conjuntos Cualitativos Dinámicos)
        self.caracteristicas = set()
        if int(self.ritmo) >= 80: self.caracteristicas.add("Veloz")
        if int(self.regate) >= 80: self.caracteristicas.add("Regateador")
        if int(self.tiro) >= 80: self.caracteristicas.add("Goleador")
        if int(self.pase) >= 80: self.caracteristicas.add("Visión")
        if int(self.edad) <= 25 and int(self.edad) > 0: self.caracteristicas.add("Joven")
        if int(self.defensa) >= 80: self.caracteristicas.add("Muralla")
        
        if not self.caracteristicas:
            self.caracteristicas = {"Consistente"}

    def obtener_vector(self):
        # Retorna el bloque de stats numéricas requeridas para el cálculo de similitud vectorial
        return [
            int(self.ritmo),
            int(self.tiro),
            int(self.pase),
            int(self.regate),
            int(self.defensa),
            int(self.fisico)
        ]

    def __str__(self):
        return f"{self.nombre} ({self.overall})"

# 2. PROCESAMIENTO Y CARGA DE ARCHIVOS (LECTOR CSV)

class LectorCSV:
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv

    def cargar_jugadores(self):
        if not os.path.exists(self.ruta_csv):
            # Fallback automático si se ejecuta desde carpetas raíz distintas en VS Code
            rutas_alternativas = [
                "dataplayers.csv", 
                os.path.join("..", "datafile", "dataplayers.csv"),
                os.path.join("datafile", "dataplayers.csv")
            ]
            for ruta in rutas_alternativas:
                if os.path.exists(ruta):
                    self.ruta_csv = ruta
                    break
            else:
                print(f"Error Crítico: No se encontró el archivo CSV en ninguna ruta estandarizada.")
                return []

        try:
            df = pd.read_csv(self.ruta_csv, sep=";", encoding="utf-8")
            jugadores = []

            for indice, row in df.iterrows():
                nombre = row.get("name")
                if pd.isna(nombre): 
                    nombre = f"Jugador_{indice}"

                equipo = row.get("team") if pd.notna(row.get("team")) else "Sin Equipo"
                if equipo == "Sin Equipo" and pd.notna(row.get("club_name")):
                    equipo = row.get("club_name")

                pais = row.get("country") if pd.notna(row.get("country")) else "Desconocida"
                posicion = row.get("best_position") if pd.notna(row.get("best_position")) else "Desconocida"

                data = {
                    "id": int(indice),
                    "nombre": str(nombre),
                    "edad": int(row.get("age", 0)) if pd.notna(row.get("age")) else 0,
                    "posicion": str(posicion),
                    "equipo": str(equipo),
                    "liga": str(pais),
                    "overall": int(row.get("best_overall_rating", 0)) if pd.notna(row.get("best_overall_rating")) else 0,
                    "potencial": int(row.get("best_overall_rating", 0)) if pd.notna(row.get("best_overall_rating")) else 0,
                    "ritmo": int(row.get("sprint_speed", 0)) if pd.notna(row.get("sprint_speed")) else 0,
                    "tiro": int(row.get("finishing", 0)) if pd.notna(row.get("finishing")) else 0,
                    "pase": int(row.get("short_passing", 0)) if pd.notna(row.get("short_passing")) else 0,
                    "regate": int(row.get("dribbling", 0)) if pd.notna(row.get("dribbling")) else 0,
                    "defensa": int(row.get("defensive_awareness", 0)) if pd.notna(row.get("defensive_awareness")) else 0,
                    "fisico": int(row.get("strength", 0)) if pd.notna(row.get("strength")) else 0,
                    "precio_aproximado": row.get("precio_aproximado", 0),
                    "valor": 0,
                    "salario": 0
                }
                jugadores.append(Jugador(data))
            return jugadores
        except Exception as e:
            print(f"Error al parsear el archivo CSV con Pandas: {e}")
            return []

# 3. INTEGRACIÓN CON BASE DE DATOS DE GRAFOS (NEO4J)

class Neo4jManager:

    def __init__(
            self,
            uri="neo4j://127.0.0.1:7687",
            usuario="neo4j",
            password="12345678"
    ):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(usuario, password)
        )

    def cerrar(self):
        self.driver.close()

    def probar_conexion(self):

        try:

            with self.driver.session() as session:

                resultado = session.run(
                    "RETURN 'Conectado' AS mensaje"
                )

                return resultado.single()["mensaje"]

        except Exception:

            return "Desconectado"

    def obtener_pagerank(self):

        query = """
        CALL gds.pageRank.stream('jugadoresGraph')
        YIELD nodeId, score

        WITH gds.util.asNode(nodeId) AS n, score

        WHERE n:Jugador

        RETURN
            n.nombre AS jugador,
            score

        ORDER BY score DESC
        """

        try:

            with self.driver.session() as session:

                resultado = session.run(query)

                return {
                    row["jugador"]: row["score"]
                    for row in resultado
                }

        except Exception:

            return {}

    def enriquecer_grafo(self):

        query = """

        MERGE (:Atributo {nombre:'Ritmo'})
        MERGE (:Atributo {nombre:'Tiro'})
        MERGE (:Atributo {nombre:'Pase'})
        MERGE (:Atributo {nombre:'Regate'})
        MERGE (:Atributo {nombre:'Defensa'})
        MERGE (:Atributo {nombre:'Fisico'})

        """

        try:

            with self.driver.session() as session:

                session.run(query)

                session.run("""
                    MATCH (j:Jugador)
                    WHERE j.ritmo >= 80
                    MATCH (a:Atributo {nombre:'Ritmo'})
                    MERGE (j)-[:DESTACA_EN]->(a)
                """)

                session.run("""
                    MATCH (j:Jugador)
                    WHERE j.tiro >= 80
                    MATCH (a:Atributo {nombre:'Tiro'})
                    MERGE (j)-[:DESTACA_EN]->(a)
                """)

                session.run("""
                    MATCH (j:Jugador)
                    WHERE j.pase >= 80
                    MATCH (a:Atributo {nombre:'Pase'})
                    MERGE (j)-[:DESTACA_EN]->(a)
                """)

                session.run("""
                    MATCH (j:Jugador)
                    WHERE j.regate >= 80
                    MATCH (a:Atributo {nombre:'Regate'})
                    MERGE (j)-[:DESTACA_EN]->(a)
                """)

                session.run("""
                    MATCH (j:Jugador)
                    WHERE j.defensa >= 80
                    MATCH (a:Atributo {nombre:'Defensa'})
                    MERGE (j)-[:DESTACA_EN]->(a)
                """)

                session.run("""
                    MATCH (j:Jugador)
                    WHERE j.fisico >= 80
                    MATCH (a:Atributo {nombre:'Fisico'})
                    MERGE (j)-[:DESTACA_EN]->(a)
                """)

            print("Grafo enriquecido correctamente.")

            return True

        except Exception as e:

            print("Error enriqueciendo grafo:", e)

            return False


# 4. CAPA ALGORÍTMICA HÍBRIDA (COSENO + JACCARD)

def coef_jaccard(conjunto_A, conjunto_B):
    interseccion = len(conjunto_A.intersection(conjunto_B))
    union = len(conjunto_A.union(conjunto_B))
    return interseccion / union if union != 0 else 0.0

class EngineRecomendacionHibrida:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        if not self.jugadores:
            self.matriz_normalizada = np.array([])
            return
        
        # Construcción de la matriz numérica escalada de rendimiento técnico
        matriz = np.array([j.obtener_vector() for j in self.jugadores])
        scaler = MinMaxScaler()
        self.matriz_normalizada = scaler.fit_transform(matriz)

    def obtener_recomendaciones(self, nombre_jugador, peso_rendimiento=0.6, peso_caracteristicas=0.4, top_n=5):
        indice_obj = next((i for i, j in enumerate(self.jugadores) if j.nombre.lower() == nombre_jugador.lower()), None)
        if indice_obj is None:
            raise ValueError(f"El jugador '{nombre_jugador}' no existe en la base de datos local.")

        jugador_obj = self.jugadores[indice_obj]
        vector_obj = self.matriz_normalizada[indice_obj]
        
        # Ejecución del algoritmo matemático de Similitud de Coseno
        similitudes_coseno = cosine_similarity([vector_obj], self.matriz_normalizada)[0]
        resultados_hibridos = []

        for i, jugador_evaluado in enumerate(self.jugadores):
            if i == indice_obj:
                continue
            
            score_coseno = similitudes_coseno[i]
            score_jaccard = coef_jaccard(jugador_obj.caracteristicas, jugador_evaluado.caracteristicas)
            
            # Ecuación compuesta ponderada según necesidades del sistema
            score_final = (score_coseno * peso_rendimiento) + (score_jaccard * peso_caracteristicas)

            resultados_hibridos.append({
                "jugador": jugador_evaluado,
                "similitud_rendimiento": score_coseno,
                "similitud_atributos": score_jaccard,
                "score_hibrido": round(score_final, 4)
            })

        # Ordenamiento descendente según el grado de match híbrido
        resultados_hibridos.sort(key=lambda x: x["score_hibrido"], reverse=True)
        return resultados_hibridos[:top_n]

# PIPELINES DE INICIALIZACIÓN GLOBAL

lector_datos = LectorCSV(os.path.join("datafile", "dataplayers.csv"))
JUGADORES_DB = lector_datos.cargar_jugadores()
NOMBRES_JUGADORES = [j.nombre for j in JUGADORES_DB] if JUGADORES_DB else []

engine_scouting = EngineRecomendacionHibrida(JUGADORES_DB) if JUGADORES_DB else None

manager_neo4j = Neo4jManager()

try:
    manager_neo4j.enriquecer_grafo()
except Exception as e:
    print("Error al enriquecer Neo4j:", e)

# 5. INTERFAZ GRÁFICA CONTROLADA (CUSTOMTKINTER HÍBRIDO)

class ScoutingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tactical Graph Scouting - Sistema Híbrido Unificado")
        self.geometry("850x720")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Variable de control de Tkinter para solventar problemas de lectura en Comboboxes dinámicos
        self.seleccion_actual_var = ctk.StringVar(value="")

        # HEADER
        self.title_label = ctk.CTkLabel(self, text="TACTICAL GRAPH SCOUTING", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(pady=15)

        # ESTADO DE RED DE DATOS
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(pady=2, padx=20, fill="x")
        conexion_neo = manager_neo4j.probar_conexion()
        color_status = "green" if conexion_neo == "Conectado" else "red"
        
        self.lbl_db = ctk.CTkLabel(
            self.status_frame, 
            text=f"Registros en Memoria: {len(JUGADORES_DB)} | Servidor Neo4j Local: {conexion_neo}",
            text_color=color_status, font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_db.pack(pady=4)

        # PANEL DE ENTRADA PREDICTIVA
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=15, padx=20, fill="x")

        self.label_instruccion = ctk.CTkLabel(self.input_frame, text="Busca y selecciona el perfil del jugador objetivo:", font=ctk.CTkFont(size=13, weight="bold"))
        self.label_instruccion.pack(pady=5)

        # 1. Cuadro de texto interactivo para la escritura libre
        self.entry_busqueda = ctk.CTkEntry(self.input_frame, width=420, placeholder_text="Escribe aquí el nombre del futbolista... (Ej: Messi / Cristiano)")
        self.entry_busqueda.pack(pady=5)
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_nombres_dinamico)

        # 2. Menú de sugerencias enlazado de forma estricta a la variable de control
        self.combo_sugerencias = ctk.CTkComboBox(
            self.input_frame, width=420, 
            values=NOMBRES_JUGADORES[:30] if NOMBRES_JUGADORES else ["Cargando..."],
            command=self.seleccionar_desde_sugerencia,
            variable=self.seleccion_actual_var
        )
        self.combo_sugerencias.pack(pady=5)

        # BOTÓN ACCIONADOR DE REPORTES
        self.btn_buscar = ctk.CTkButton(
            self, text="⚡ Generar Informe de Recomendación Híbrida", 
            command=self.ejecutar_analisis_hibrido, font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.btn_buscar.pack(pady=10)

        # CONTENEDOR DE INFORME TÉCNICO UNIFICADO
        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.lbl_reporte = ctk.CTkLabel(self.result_frame, text="📋 Ficha Técnica y Reporte Compuesto de Reclutamiento", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_reporte.pack(pady=6)

        self.txt_resultados = ctk.CTkTextbox(self.result_frame, font=ctk.CTkFont(family="Courier", size=12))
        self.txt_resultados.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Texto instructivo inicial de la pantalla
        self.txt_resultados.configure(state="normal")
        self.txt_resultados.insert("1.0", "Escribe el nombre de un jugador arriba, selecciónalo en la lista desplegable y presiona el botón para calcular las recomendaciones híbridas.")
        self.txt_resultados.configure(state="disabled")

    # CONTROLADOR EN TIEMPO REAL DEL AUTOCOMPLETADO
    def filtrar_nombres_dinamico(self, event):
        texto_ingresado = self.entry_busqueda.get().strip().lower()
        
        if not texto_ingresado:
            coincidencias = NOMBRES_JUGADORES[:30]
        else:
            coincidencias = [nombre for nombre in NOMBRES_JUGADORES if texto_ingresado in nombre.lower()]
        
        if coincidencias:
            self.combo_sugerencias.configure(values=coincidencias)
            self.seleccion_actual_var.set(coincidencias[0])
        else:
            self.combo_sugerencias.configure(values=["No hay coincidencias"])
            self.seleccion_actual_var.set("No hay coincidencias")

    def seleccionar_desde_sugerencia(self, seleccion):
        if seleccion != "No hay coincidencias":
            self.entry_busqueda.delete(0, ctk.END)
            self.entry_busqueda.insert(0, seleccion)

    # INTERFACES LOGÍCO-MATEMÁTICAS 
    def ejecutar_analisis_hibrido(self):
        # Leemos directo de la variable de control para evitar fallos de refresco de CustomTkinter
        jugador_sel = self.seleccion_actual_var.get().strip()

        # Si el usuario escribió completo pero no interactuó con el combo, respaldamos con la caja de texto
        if not jugador_sel or jugador_sel == "No hay coincidencias":
            jugador_sel = self.entry_busqueda.get().strip()

        # Validación estricta de existencia contra los nombres reales indexados del CSV
        jugador_match_oficial = next((nombre for nombre in NOMBRES_JUGADORES if nombre.lower() == jugador_sel.lower()), None)

        if not jugador_match_oficial:
            messagebox.showwarning("Jugador Inválido", f"El jugador '{jugador_sel}' no se encuentra en la base de datos o no ha sido seleccionado correctamente de las sugerencias.")
            return

        # Consulta dinámica del estado actual del Grafo en Neo4j
        diccionario_pagerank = manager_neo4j.obtener_pagerank()

        # Habilitación temporal de escritura en pantalla
        self.txt_resultados.configure(state="normal")
        self.txt_resultados.delete("1.0", ctk.END)

        # Extracción del objeto completo origen
        jugador_origen = next(j for j in JUGADORES_DB if j.nombre == jugador_match_oficial)

        # CONSTRUCCIÓN VISUAL DEL INFORME TÉCNICO EN EL COMPONENTE TEXTBOX
        reporte = f"             INFORME TÉCNICO DE RECLUTAMIENTO - MÉTODO HÍBRIDO             \n"
        reporte += f" JUGADOR BASE ANALIZADO:\n"
        reporte += f" 👤 Nombre:    {jugador_origen.nombre}\n"
        reporte += f" 🏢 Club/Liga: {jugador_origen.equipo} ({jugador_origen.liga})\n"
        reporte += f" 🛡️ Posición:  {jugador_origen.posicion} | Val. Media: {jugador_origen.overall}\n"
        reporte += f" 🧬 Rasgos Cualitativos: {list(jugador_origen.caracteristicas)}\n"
        reporte += f" 📊 Stats Base [Rit, Tir, Pas, Reg, Def, Fis]: {jugador_origen.obtener_vector()}\n"
        reporte += f"\n" + "="*75 + "\n"
        reporte += f" TOP 5 ALTERNATIVAS SUGERIDAS (60% Rendimiento Técnico + 40% Rasgos):\n"
        reporte += f"===========================================================================\n\n"

        if engine_scouting:
            try:
                # Ejecución de la recomendación combinada ponderada
                recomendaciones = engine_scouting.obtener_recomendaciones(jugador_match_oficial, peso_rendimiento=0.6, peso_caracteristicas=0.4, top_n=5)
                
                for i, item in enumerate(recomendaciones, start=1):
                    j = item["jugador"]
                    match_global = item["score_hibrido"] * 100
                    match_coseno = item["similitud_rendimiento"] * 100
                    match_jaccard = item["similitud_atributos"] * 100
                    
                    # Extracción del índice de prestigio calculado por PageRank en Neo4j
                    score_page_rank = diccionario_pagerank.get(j.nombre, 0.1500)

                    reporte += f" {i}. {j.nombre} ({j.equipo} - {j.liga})\n"
                    reporte += f"    MATCH GLOBAL COMPUESTO: {match_global:.2f}%\n"
                    reporte += f"     ↳ Similitud de Rendimiento: {match_coseno:.1f}%\n"
                    reporte += f"     ↳ Similitud Cualitativa:   {match_jaccard:.1f}%\n"
                    reporte += f"    Etiquetas de Perfil: {list(j.caracteristicas)}\n"
                    reporte += f"    Centralidad en Red de Fichajes (PageRank Score): {score_page_rank:.4f}\n"
                    reporte += f"    -----------------------------------------------------------------------\n"
            except Exception as e:
                reporte += f"Error durante el cálculo algorítmico: {e}\n"
        else:
            reporte += "El motor matemático híbrido no pudo inicializarse correctamente por falta de datos.\n"

        self.txt_resultados.insert("1.0", reporte)
        self.txt_resultados.configure(state="disabled")

# =====================================================================
# PUNTO DE ENTRADA PRINCIPAL DEL PROGRAMA
# =====================================================================
if __name__ == "__main__":
    app = ScoutingApp()
    try:
        app.mainloop()
    finally:
        manager_neo4j.cerrar()