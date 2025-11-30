import math

class Process:
    def __init__(self, pid, size):
        self.id = pid
        self.size = size
        # Calculamos páginas necesarias (suponiendo page_size=256 por defecto si no se pasa)
        # En la integración real, esto se ajustará mejor.
        self.num_pages = math.ceil(size / 256)