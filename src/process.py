import math


class Process:
    def __init__(self, pid, size, page_size=256):
        # Mantenemos compatibilidad con todos:
        self.id = pid  # Para que simulator.py no llore
        self.pid = pid  # Para que paging.py no llore

        self.size = size
        self.page_size = page_size

        # Calcular páginas necesarias
        self.num_pages = math.ceil(size / page_size)

        # Inicializar tabla de páginas
        self.page_table = {}
        self.init_page_table()

    def init_page_table(self):
        for i in range(self.num_pages):
            self.page_table[i] = {
                'frame_id': None,
                'location': None,  # 'RAM', 'SWAP' o None
                'present': False  # True solo si esta en RAM
            }

    def update_page_status(self, page_number, frame_id, location):
        if page_number in self.page_table:
            self.page_table[page_number]['frame_id'] = frame_id
            self.page_table[page_number]['location'] = location
            self.page_table[page_number]['present'] = (location == 'RAM')
        else:
            print(f"Error: La pagina {page_number} no existe en el proceso {self.pid}")

    def show_page_table(self):
        print(f"\n--- Tabla de Paginas: Proceso ID {self.pid} ---")
        print(f"Tamaño: {self.size} bytes | Total Paginas: {self.num_pages}")
        print("-" * 60)
        print(f"{'Pagina':<10} | {'Ubicacion':<10} | {'Marco Fisico':<15} | {'En RAM':<10}")
        print("-" * 60)

        for page, info in self.page_table.items():
            loc = info['location'] if info['location'] else "Pendiente"
            fid = info['frame_id'] if info['frame_id'] is not None else "-"
            present = "Si" if info['present'] else "No"

            print(f"{page:<10} | {loc:<10} | {fid:<15} | {present:<10}")
        print("-" * 60)

    def __repr__(self):
        return f"<Proceso {self.pid}: {self.size} bytes ({self.num_pages} pags)>"