class Jugador:

    def __init__(self, data):

        # Identificación
        self.id = data.get("id")
        self.nombre = data.get("nombre")

        # Información general
        self.edad = data.get("edad")
        self.posicion = data.get("posicion")
        self.equipo = data.get("equipo")
        self.liga = data.get("liga")

        # Ratings FIFA
        self.overall = data.get("overall")
        self.potencial = data.get("potencial")

        # Estadísticas principales
        self.ritmo = data.get("ritmo")
        self.tiro = data.get("tiro")
        self.pase = data.get("pase")
        self.regate = data.get("regate")
        self.defensa = data.get("defensa")
        self.fisico = data.get("fisico")

        # Economía
        self.valor = data.get("valor")
        self.salario = data.get("salario")

    def obtener_vector(self):
        #Convierte los atributos del jugador en un vector numérico.

        return [

            self.edad,
            self.overall,
            self.potencial,

            self.ritmo,
            self.tiro,
            self.pase,
            self.regate,
            self.defensa,
            self.fisico
        ]

    def __str__(self):

        return (
            f"{self.nombre} | "
            f"{self.equipo} | "
            f"{self.posicion}"
        )