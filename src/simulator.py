import config_loader
from memory import MemoryManager
# Importamos los módulos de tus compañeros (usaremos los dummies que te pasé por ahora)
# Cuando ellos te pasen los reales, NO necesitas cambiar nada aquí.
from process import Process
from paging import PagingSystem


class OSSimulator:
    def __init__(self):
        # 1. Cargar configuración
        self.config = config_loader.load_config("config.ini")

        # 2. Inicializar tu MemoryManager real
        # config_loader devuelve 'frames_ram' y 'frames_swap' ya calculados
        self.memory = MemoryManager(self.config['frames_ram'], self.config['frames_swap'])

        # 3. Inicializar Paging (Le pasamos la memoria y el tamaño de página)
        self.paging = PagingSystem(self.memory, self.config['page_size'])

        self.processes = {}  # Diccionario para guardar procesos activos {pid: Process}
        self.pid_counter = 1

    def create_process(self, size_bytes):
        # Crear proceso (Lógica de Roberto)
        new_process = Process(self.pid_counter, size_bytes)

        print(f"\n[Simulador] Creando Proceso {new_process.id} ({size_bytes} bytes)...")
        print(f"[Simulador] Requiere {new_process.num_pages} páginas.")

        # Cargar proceso usando Paging (Lógica de Sergio)
        success = self.paging.load_process(new_process)

        if success:
            self.processes[self.pid_counter] = new_process
            print(f"[Exito] Proceso {self.pid_counter} cargado en memoria.")
            self.pid_counter += 1
        else:
            print(f"[Error] Fallo al cargar Proceso {self.pid_counter} (Memoria llena o error interno).")

    def terminate_process(self, pid):
        if pid in self.processes:
            # Paging se encarga de liberar marcos
            self.paging.unload_process(pid)
            del self.processes[pid]
            print(f"[Simulador] Proceso {pid} terminado correctamente.")
        else:
            print(f"[Error] El proceso {pid} no existe.")

    def show_memory_status(self):
        # Usamos tus métodos de visualización de memory.py
        self.memory.print_ram()
        self.memory.print_swap()

    def show_page_table(self, pid):
        if pid in self.processes:
            # Esto lo maneja Sergio en Paging
            self.paging.print_page_table(pid)
        else:
            print("Proceso no encontrado.")

    def get_global_stats(self):
        # 1. Calcular Marcos Libres en RAM
        # Accedemos a la lista .ram de tu MemoryManager y contamos los .free
        free_ram = sum(1 for frame in self.memory.ram if frame.free)
        total_ram = len(self.memory.ram)

        # 2. Calcular Uso de Swap
        # Contamos cuántos marcos de swap están ocupados (no free)
        used_swap = sum(1 for frame in self.memory.swap if not frame.free)
        total_swap = len(self.memory.swap)

        # 3. Fallos de página (Page Faults)
        # Intentamos leerlo del sistema de paginación (si Sergio lo implementa)
        # Si no existe (porque usamos el dummy), mostramos 0
        page_faults = getattr(self.paging, 'page_faults', 0)

        return {
            "Marcos RAM Libres": f"{free_ram} / {total_ram}",
            "Uso de Swap": f"{used_swap} / {total_swap}",
            "Fallos de Página": page_faults
        }