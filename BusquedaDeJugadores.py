import customtkinter as ctk
from tkinter import messagebox

# =====================================================================
# DATASET SIMULADO (Top 3 Ligas: España, Inglaterra, Alemania)
# =====================================================================
# Base de datos inicial para que el sistema tenga con qué operar.
# Despues lo cambiaremos por el csv con los datos que nos pasaron
JUGADORES_DB = [
    {
        "nombre": "Lamine Yamal", "liga": "LaLiga", "posicion": "Extremo",
        "caracteristicas": {"Zurdo", "Regateador", "Joven", "Veloz"},
        "stats": [92, 78, 85, 30], "pagerank": 0.85
    },
    {
        "nombre": "Jamal Musiala", "liga": "Bundesliga", "posicion": "MCO",
        "caracteristicas": {"Diestro", "Regateador", "Agil", "Joven"},
        "stats": [88, 82, 88, 40], "pagerank": 0.88
    },
    {
        "nombre": "Bukayo Saka", "liga": "Premier League", "posicion": "Extremo",
        "caracteristicas": {"Zurdo", "Regateador", "Consistente", "Veloz"},
        "stats": [89, 84, 82, 55], "pagerank": 0.82
    },
    {
        "nombre": "Florian Wirtz", "liga": "Bundesliga", "posicion": "MCO",
        "caracteristicas": {"Diestro", "Visión", "Agil", "Joven"},
        "stats": [82, 80, 90, 45], "pagerank": 0.86
    },
    {
        "nombre": "Cole Palmer", "liga": "Premier League", "posicion": "MCO",
        "caracteristicas": {"Zurdo", "Visión", "Goleador", "Joven"},
        "stats": [80, 85, 84, 38], "pagerank": 0.80
    }
]

# =====================================================================
# SECCIÓN DE ALGORITMOS (Tu parte: Jaccard)
# =====================================================================

def coef_jaccard(conjunto_A, conjunto_B):
    """
    Calcula el Coeficiente de Jaccard entre dos conjuntos de características.
    Fórmula: J(A, B) = |A ∩ B| / |A ∪ B|
    """
    interseccion = len(conjunto_A.intersection(conjunto_B))
    union = len(conjunto_A.union(conjunto_B))
    
    if union == 0:
        return 0.0
    return interseccion / union

def buscar_por_jaccard(jugador_objetivo_nombre):
    """
    Busca y ordena a los jugadores candidatos basados en la similitud
    de Jaccard respecto a un jugador objetivo.
    """
    # Encontrar el perfil del jugador objetivo
    jugador_obj = next((j for j in JUGADORES_DB if j["nombre"].lower() == jugador_objetivo_nombre.lower()), None)
    
    if not jugador_obj:
        return None
        
    resultados = []
    for jugador in JUGADORES_DB:
        if jugador["nombre"].lower() != jugador_obj["nombre"].lower():
            # Mandamos a llamar a tu algoritmo
            similitud = calcular_jaccard(jugador_obj["caracteristicas"], jugador["caracteristicas"])
            resultados.append((jugador["nombre"], similitud, jugador["liga"], jugador["posicion"]))
            
    # Ordenar de mayor a menor similitud
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados

# =====================================================================
# ESPACIO PARA TUS COMPAÑEROS (Stubs)
# =====================================================================
def calcular_coseno_knn():
    # Aquí Julio o Pipo meterán su lógica de vectores estadísticos
    pass

def calcular_pagerank():
    # Aquí meterán la jerarquía de red con Neo4j
    pass


# =====================================================================
# INTERFAZ GRÁFICA (Menú Bonito y Funcional)
# =====================================================================
class ScoutingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Tactical Graph Scouting - Sistema de Recomendación")
        self.geometry("750x550")
        ctk.set_appearance_mode("dark")  # Modo oscuro elegante
        ctk.set_default_color_theme("green")  # Estética de cancha/fútbol

        # --- PANEL DE TÍTULO ---
        self.title_label = ctk.CTkLabel(self, text="⚽ TACTICAL GRAPH SCOUTING", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # --- CONTENEDOR DE ENTRADA ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.label_instruccion = ctk.CTkLabel(self.input_frame, text="Selecciona o escribe un jugador base:", font=ctk.CTkFont(size=14))
        self.label_instruccion.pack(pady=5)

        # Dropdown para elegir el jugador base de forma rápida
        opciones_jugadores = [j["nombre"] for j in JUGADORES_DB]
        self.combo_jugadores = ctk.CTkComboBox(self.input_frame, values=opciones_jugadores, width=300)
        self.combo_jugadores.pack(pady=10)

        # --- BOTÓN DE ACCIÓN ---
        self.btn_buscar = ctk.CTkButton(self, text="Calcular Recomendaciones (Jaccard)", command=self.ejecutar_scouting, font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_buscar.pack(pady=15)

        # --- ÁREA DE RESULTADOS ---
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.label_resultados = ctk.CTkLabel(self.results_frame, text="Resultados del Análisis Táctico:", font=ctk.CTkFont(size=14, weight="bold"))
        self.label_resultados.pack(pady=5)

        # TextBox con scroll para mostrar de forma limpia los datos
        self.textbox_resultados = ctk.CTkTextbox(self.results_frame, font=ctk.CTkFont(size=13), activate_scrollbars=True)
        self.textbox_resultados.pack(pady=10, padx=10, fill="both", expand=True)
        self.textbox_resultados.configure(state="disabled")

    def ejecutar_scouting(self):
        jugador_seleccionado = self.combo_jugadores.get()
        
        if not jugador_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un jugador válido.")
            return

        # Llamada a tu algoritmo
        lista_recomendaciones = buscar_por_jaccard(jugador_seleccionado)

        # Habilitar caja de texto para actualizar contenido
        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("1.0", ctk.END)

        if lista_recomendaciones:
            texto_pantalla = f"Analizando clones tácticos para: {jugador_seleccionado}\n"
            texto_pantalla += "="*60 + "\n\n"
            
            for rank, (nombre, similitud, liga, posicion) in enumerate(lista_recomendaciones, 1):
                porcentaje = similitud * 100
                texto_pantalla += f"{rank}. {nombre} ({posicion})\n"
                texto_pantalla += f"   📍 Liga: {liga}\n"
                texto_pantalla += f"   🧬 Afinidad de Perfil (Jaccard): {porcentaje:.1f}%\n"
                texto_pantalla += "-"*40 + "\n"
        else:
            texto_pantalla = "No se encontró información suficiente para el análisis."

        self.textbox_resultados.insert("1.0", texto_pantalla)
        # Bloquear de nuevo para que el usuario no edite los resultados manualmente
        self.textbox_resultados.configure(state="disabled")

# no estoy seguro si esta onda se tendria que usar pero por si acaso repasemosla o veamos si la quitamos porque nunca la vimos
if __name__ == "__main__":
    app = ScoutingApp()
    app.mainloop()