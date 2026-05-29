import customtkinter as ctk
from tkinter import messagebox

# =====================================================================
# DATASET SIMULADO
# =====================================================================

JUGADORES_DB = [
    {
        "nombre": "Lamine Yamal",
        "liga": "LaLiga",
        "posicion": "Extremo",
        "caracteristicas": {"Zurdo", "Regateador", "Joven", "Veloz"},
        "stats": [92, 78, 85, 30],
        "pagerank": 0.85
    },
    {
        "nombre": "Jamal Musiala",
        "liga": "Bundesliga",
        "posicion": "MCO",
        "caracteristicas": {"Diestro", "Regateador", "Agil", "Joven"},
        "stats": [88, 82, 88, 40],
        "pagerank": 0.88
    },
    {
        "nombre": "Bukayo Saka",
        "liga": "Premier League",
        "posicion": "Extremo",
        "caracteristicas": {"Zurdo", "Regateador", "Consistente", "Veloz"},
        "stats": [89, 84, 82, 55],
        "pagerank": 0.82
    },
    {
        "nombre": "Florian Wirtz",
        "liga": "Bundesliga",
        "posicion": "MCO",
        "caracteristicas": {"Diestro", "Visión", "Agil", "Joven"},
        "stats": [82, 80, 90, 45],
        "pagerank": 0.86
    },
    {
        "nombre": "Cole Palmer",
        "liga": "Premier League",
        "posicion": "MCO",
        "caracteristicas": {"Zurdo", "Visión", "Goleador", "Joven"},
        "stats": [80, 85, 84, 38],
        "pagerank": 0.80
    }
]

# =====================================================================
# ALGORITMO JACCARD
# =====================================================================

def coef_jaccard(conjunto_A, conjunto_B):
    """
    Calcula la similitud de Jaccard entre dos conjuntos.
    """

    interseccion = len(conjunto_A.intersection(conjunto_B))
    union = len(conjunto_A.union(conjunto_B))

    if union == 0:
        return 0.0

    return interseccion / union


def buscar_por_jaccard(jugador_objetivo_nombre):
    """
    Busca jugadores similares usando Jaccard.
    """

    jugador_obj = next(
        (
            j for j in JUGADORES_DB
            if j["nombre"].lower() == jugador_objetivo_nombre.lower()
        ),
        None
    )

    if not jugador_obj:
        return []

    resultados = []

    for jugador in JUGADORES_DB:

        # Evitar comparar consigo mismo
        if jugador["nombre"].lower() != jugador_obj["nombre"].lower():

            similitud = coef_jaccard(
                jugador_obj["caracteristicas"],
                jugador["caracteristicas"]
            )

            resultados.append({
                "nombre": jugador["nombre"],
                "liga": jugador["liga"],
                "posicion": jugador["posicion"],
                "similitud": similitud
            })

    # Ordenar de mayor a menor
    resultados.sort(key=lambda x: x["similitud"], reverse=True)

    return resultados


# =====================================================================
# STUBS FUTUROS
# =====================================================================

def calcular_coseno_knn():
    pass


def calcular_pagerank():
    pass


# =====================================================================
# INTERFAZ
# =====================================================================

class ScoutingApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("⚽ Tactical Graph Scouting")
        self.geometry("750x550")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # TÍTULO
        self.title_label = ctk.CTkLabel(
            self,
            text="TACTICAL GRAPH SCOUTING",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)

        # FRAME INPUT
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.label_instruccion = ctk.CTkLabel(
            self.input_frame,
            text="Selecciona un jugador:",
            font=ctk.CTkFont(size=14)
        )
        self.label_instruccion.pack(pady=5)

        opciones_jugadores = [j["nombre"] for j in JUGADORES_DB]

        self.combo_jugadores = ctk.CTkComboBox(
            self.input_frame,
            values=opciones_jugadores,
            width=300
        )

        self.combo_jugadores.pack(pady=10)

        # BOTÓN
        self.btn_buscar = ctk.CTkButton(
            self,
            text="Buscar Similares",
            command=self.ejecutar_scouting,
            font=ctk.CTkFont(size=14, weight="bold")
        )

        self.btn_buscar.pack(pady=15)

        # RESULTADOS
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.textbox_resultados = ctk.CTkTextbox(
            self.results_frame,
            font=ctk.CTkFont(size=13)
        )

        self.textbox_resultados.pack(
            pady=10,
            padx=10,
            fill="both",
            expand=True
        )

        self.textbox_resultados.configure(state="disabled")

    # =================================================================

    def ejecutar_scouting(self):

        jugador_seleccionado = self.combo_jugadores.get()

        if not jugador_seleccionado:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona un jugador válido."
            )
            return

        resultados = buscar_por_jaccard(jugador_seleccionado)

        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("1.0", ctk.END)

        if resultados:

            texto = f"🔎 Similares a: {jugador_seleccionado}\n"
            texto += "=" * 50 + "\n\n"

            for i, jugador in enumerate(resultados[:3], start=1):

                porcentaje = jugador["similitud"] * 100

                texto += f"{i}. {jugador['nombre']}\n"
                texto += f"   ⚽ Posición: {jugador['posicion']}\n"
                texto += f"   🌍 Liga: {jugador['liga']}\n"
                texto += f"   🧬 Similitud Jaccard: {porcentaje:.1f}%\n"
                texto += "-" * 40 + "\n"

        else:
            texto = "No se encontraron resultados."

        self.textbox_resultados.insert("1.0", texto)
        self.textbox_resultados.configure(state="disabled")


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    app = ScoutingApp()
    app.mainloop()
