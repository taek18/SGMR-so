class PagingSystem:
    def __init__(self, memory_manager, page_size):
        self.memory = memory_manager
        self.page_size = page_size
        # Simulación de tabla de páginas: {pid: [lista de frames]}
        self.page_tables = {}

    def load_process(self, process):
        # DUMMY: Simplemente intenta asignar en RAM secuencialmente para probar
        frames_assigned = []
        for i in range(process.num_pages):
            # Usamos tu método allocate_ram de memory.py
            frame_id, error = self.memory.allocate_ram(process.id, i)

            if error == "NO_SPACE":
                # Aquí iría la lógica FIFO de Sergio,
                # por ahora solo devolvemos False si se llena
                print(" [Paging-Dummy] RAM llena, se necesitaría Swap/FIFO aquí.")
                return False

            frames_assigned.append(frame_id)

        self.page_tables[process.id] = frames_assigned
        return True

    def unload_process(self, pid):
        if pid in self.page_tables:
            frames = self.page_tables[pid]
            for f_id in frames:
                self.memory.free_ram_frame(f_id)
            del self.page_tables[pid]

    def print_page_table(self, pid):
        if pid in self.page_tables:
            print(f"Páginas del proceso {pid} -> Marcos RAM: {self.page_tables[pid]}")
        else:
            print("Proceso no tiene tabla asignada.")