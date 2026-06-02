import csv
import os
from tkinter import messagebox
import customtkinter as ctk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# =====================================================================
# CLASE MODELO DE JUGADOR
# =====================================================================


class Jugador:

    def __init__(self, nombre, liga, posicion, caracteristicas, stats, pagerank):
        self.nombre = nombre
        self.liga = liga
        self.posicion = posicion
        # Se guarda como conjunto para el coeficiente de Jaccard
        self.caracteristicas = set(caracteristicas)
        # Lista de enteros/flotantes para similitud de coseno
        self.stats = stats
        self.pagerank = float(pagerank)

    def obtener_vector(self):
        return self.stats


# =====================================================================
# LECTOR NATIVO DE BASE DE DATOS (CSV REAL)
# =====================================================================


def cargar_jugadores_desde_csv():
    """
    Busca el CSV descargado en la subcarpeta datafile y mapea los objetos.
    """
    ruta_csv = os.path.join("datafile", "dataplayers.csv")
    jugadores_lista = []

    if not os.path.exists(ruta_csv):
        # Fallback por si ejecutas directamente desde la raíz sin subcarpeta
        ruta_csv = "dataplayers.csv"
        if not os.path.exists(ruta_csv):
            return []

    try:
        with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Parsear características separadas por comas en el CSV
                caract = [c.strip() for c in fila["caracteristicas"].split(",")]

                # Extraer stats numéricas del CSV (ej: ritmo, tiro, pase, defensa)
                stats = [
                    float(fila["stat1"]),
                    float(fila["stat2"]),
                    float(fila["stat3"]),
                    float(fila["stat4"]),
                ]

                j = Jugador(
                    nombre=fila["nombre"],
                    liga=fila["liga"],
                    posicion=fila["posicion"],
                    caracteristicas=caract,
                    stats=stats,
                    pagerank=fila.get("pagerank", 0.0),
                )
                jugadores_lista.append(j)
    except Exception as e:
        print(f"Error leyendo el dataset: {e}")

    return jugadores_lista


# Carga global de los 541 jugadores del CSV real
JUGADORES_DB = cargar_jugadores_desde_csv()

# =====================================================================
# ALGORITMO 1: COEFICIENTE DE JACCARD
# =====================================================================


def coef_jaccard(conjunto_A, conjunto_B):
    interseccion = len(conjunto_A.intersection(conjunto_B))
    union = len(conjunto_A.union(conjunto_B))
    return interseccion / union if union != 0 else 0.0


def buscar_por_jaccard(jugador_objetivo_nombre):
    jugador_obj = next(
        (
            j
            for j in JUGADORES_DB
            if j.nombre.lower() == jugador_objetivo_nombre.lower()
        ),
        None,
    )
    if not jugador_obj:
        return []

    resultados = []
    for jugador in JUGADORES_DB:
        if jugador.nombre.lower() != jugador_obj.nombre.lower():
            similitud = coef_jaccard(
                jugador_obj.caracteristicas, jugador.caracteristicas
            )
            resultados.append({"jugador": jugador, "similitud": similitud})

    resultados.sort(key=lambda x: x["similitud"], reverse=True)
    return resultados


# =====================================================================
# ALGORITMO 2: SIMILITUD DE COSENO (AÑADIDO)
# =====================================================================


class SimilitudCoseno:

    def __init__(self, jugadores):
        self.jugadores = jugadores
        if not self.jugadores:
            self.matriz_normalizada = np.array([])
            return

        matriz = np.array([jugador.obtener_vector() for jugador in self.jugadores])
        scaler = MinMaxScaler()
        self.matriz_normalizada = scaler.fit_transform(matriz)

    def encontrar_similares(self, nombre_jugador, top_n=5):
        indice_objetivo = None
        for i, jugador in enumerate(self.jugadores):
            if jugador.nombre.lower() == nombre_jugador.lower():
                indice_objetivo = i
                break

        if indice_objetivo is None:
            raise ValueError("Jugador no encontrado")

        vector_objetivo = self.matriz_normalizada[indice_objetivo]
        similitudes = cosine_similarity(
            [vector_objetivo], self.matriz_normalizada
        )[0]

        resultados = []
        for i, score in enumerate(similitudes):
            if i != indice_objetivo:
                resultados.append(
                    {"jugador": self.jugadores[i], "similitud": round(score, 4)}
                )

        resultados.sort(key=lambda x: x["similitud"], reverse=True)
        return resultados[:top_n]


# Inicializar motor de coseno sobre los datos cargados del CSV
if JUGADORES_DB:
    motor_coseno = SimilitudCoseno(JUGADORES_DB)
else:
    motor_coseno = None

# =====================================================================
# STUBS FUTUROS: K-NN Y PAGERANK
# =====================================================================


def calcular_knn_agrupacion():
    pass


def conectar_neo4j_pagerank():
    pass


# =====================================================================
# INTERFAZ GRÁFICA EVOLUCIONADA
# =====================================================================


class ScoutingApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("⚽ Tactical Graph Scouting - Sistema Híbrido")
        self.geometry("800://650")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # ENCABEZADO
        self.title_label = ctk.CTkLabel(
            self,
            text="TACTICAL GRAPH SCOUTING",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.title_label.pack(pady=15)

        # SELECCIÓN DE JUGADOR
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=5, padx=20, fill="x")

        self.label_instruccion = ctk.CTkLabel(
            self.input_frame,
            text="Selecciona un perfil de jugador base (Dataset Real):",
            font=ctk.CTkFont(size=13),
        )
        self.label_instruccion.pack(pady=5)

        # Cargar los nombres reales dinámicamente desde el CSV
        opciones_jugadores = (
            [j.nombre for j in JUGADORES_DB]
            if JUGADORES_DB
            else ["Error cargando CSV"]
        )

        self.combo_jugadores = ctk.CTkComboBox(
            self.input_frame, values=opciones_jugadores, width=350
        )
        self.combo_jugadores.pack(pady=8)

        self.btn_buscar = ctk.CTkButton(
            self,
            text="Ejecutar Análisis Híbrido",
            command=self.ejecutar_scouting_completo,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.btn_buscar.pack(pady=10)

        # DISEÑO DE PESTAÑAS (TABVIEW) PARA MOSTRAR AMBOS ENFOQUES
        self.tab_control = ctk.CTkTabview(self)
        self.tab_control.pack(pady=10, padx=20, fill="both", expand=True)

        self.tab_control.add("Atributos (Jaccard)")
        self.tab_control.add("Rendimiento (Coseno)")

        # TextBox Pestaña Jaccard
        self.txt_jaccard = ctk.CTkTextbox(
            self.tab_control.tab("Atributos (Jaccard)"),
            font=ctk.CTkFont(size=13),
        )
        self.txt_jaccard.pack(fill="both", expand=True, padx=5, pady=5)
        self.txt_jaccard.configure(state="disabled")

        # TextBox Pestaña Coseno
        self.txt_coseno = ctk.CTkTextbox(
            self.tab_control.tab("Rendimiento (Coseno)"),
            font=ctk.CTkFont(size=13),
        )
        self.txt_coseno.pack(fill="both", expand=True, padx=5, pady=5)
        self.txt_coseno.configure(state="disabled")

    def ejecutar_scouting_completo(self):
        jugador_sel = self.combo_jugadores.get()

        if not jugador_sel or jugador_sel == "Error cargando CSV":
            messagebox.showwarning("Advertencia", "Selecciona un jugador real.")
            return

        # 1. EJECUTAR JACCARD
        res_jaccard = buscar_por_jaccard(jugador_sel)
        self.txt_jaccard.configure(state="normal")
        self.txt_jaccard.delete("1.0", ctk.END)

        texto_j = f"🔎 SIMILITUD CUALITATIVA (JACCARD) para: {jugador_sel}\n"
        texto_j += "=" * 60 + "\n\n"
        if res_jaccard:
            for i, item in enumerate(res_jaccard[:5], start=1):
                jugador = item["jugador"]
                porcentaje = item["similitud"] * 100
                texto_j += f"{i}. {jugador.nombre} ({jugador.liga})\n"
                texto_j += f"   🛡️ Posición: {jugador.posicion} | 🧬 Similitud: {porcentaje:.1f}%\n"
                texto_j += f"   ✨ Atributos: {jugador.caracteristicas}\n"
                texto_j += "-" * 50 + "\n"
        self.txt_jaccard.insert("1.0", texto_j)
        self.txt_jaccard.configure(state="disabled")

        # 2. EJECUTAR COSENO
        self.txt_coseno.configure(state="normal")
        self.txt_coseno.delete("1.0", ctk.END)

        texto_c = f"📊 SIMILITUD CUANTITATIVA (COSENO VECTORIAL) para: {jugador_sel}\n"
        texto_c += "=" * 60 + "\n\n"

        if motor_coseno:
            try:
                res_coseno = motor_coseno.encontrar_similares(
                    jugador_sel, top_n=5
                )
                for i, item in enumerate(res_coseno, start=1):
                    jugador = item["jugador"]
                    porcentaje = item["similitud"] * 100
                    texto_c += f"{i}. {jugador.nombre} ({jugador.liga})\n"
                    texto_c += f"   📈 Vector de Stats: {jugador.stats}\n"
                    texto_c += f"   🎯 Match de Rendimiento: {porcentaje:.1f}%\n"
                    texto_c += "-" * 50 + "\n"
            except Exception as e:
                texto_c += f"Error al procesar matrices: {e}"
        else:
            texto_c += "Motor de Coseno no inicializado."

        self.txt_coseno.insert("1.0", texto_c)
        self.txt_coseno.configure(state="disabled")


# =====================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =====================================================================

if __name__ == "__main__":
    if not JUGADORES_DB:
        print(
            "⚠️ ¡Alerta! No se pudo leer 'datafile/dataplayers.csv'. Revisa la ubicación."
        )
    app = ScoutingApp()
    app.mainloop()