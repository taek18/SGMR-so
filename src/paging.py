class PagingSystem:
    def __init__(self, memory_manager, page_size):
        """
        Inicializa el sistema de paginación.
        :param memory_manager: Instancia de la clase MemoryManager (memory.py)
        :param page_size: Tamaño de página definido en config.ini
        """
        self.memory = memory_manager
        self.page_size = page_size
        self.active_processes = {}

    def load_process(self, process):
        """
        Carga un proceso en memoria. Si la RAM está llena, aplica FIFO.
        """
        print(f"[Paging] Cargando proceso {process.pid} ({process.num_pages} pags)...")
        self.active_processes[process.pid] = process

        for i in range(process.num_pages):
            # 1. Intentar asignar en RAM
            frame_id, error = self.memory.allocate_ram(process.pid, i)

            if error == "NO_SPACE":
                print(f"   [!] RAM llena (Pag {i}). Ejecutando FIFO...")

                # A) Seleccionar víctima
                victim_frame_id = self.memory.select_victim_fifo()
                if victim_frame_id is None:
                    print("Error: No se pudo seleccionar víctima para Swap.")
                    return False

                # B) Identificar dueño del marco
                victim_frame = self.memory.ram[victim_frame_id]
                victim_pid = victim_frame.process_id
                victim_page_num = victim_frame.page_number

                # C) Mover a Swap
                swap_id, swap_err = self.memory.move_ram_to_swap(victim_frame_id)
                if swap_err:
                    print(f"Error: Swap lleno. No se puede realizar intercambio.")
                    return False

                print(f"      > SwapOut: Marco {victim_frame_id} (P{victim_pid}) -> Swap {swap_id}")

                # D) Actualizar tabla de páginas de la víctima
                if victim_pid in self.active_processes:
                    self.active_processes[victim_pid].update_page_status(victim_page_num, swap_id, 'SWAP')

                # E) Asignar el marco liberado al proceso actual
                frame_id, error = self.memory.allocate_ram(process.pid, i)
                if error:
                    return False

            # Actualizar tabla del proceso actual (ahora tiene marco en RAM)
            process.update_page_status(i, frame_id, 'RAM')

        print(f"[Paging] Proceso {process.pid} listo.")
        return True

    def unload_process(self, pid):
        """
        Termina un proceso y libera TODOS sus recursos (RAM y Swap).
        """
        if pid in self.active_processes:
            process = self.active_processes[pid]

            # Recorremos la tabla para liberar lo que tenga asignado
            for page_num, info in process.page_table.items():

                # Liberar RAM
                if info['location'] == 'RAM' and info['frame_id'] is not None:
                    self.memory.free_ram_frame(info['frame_id'])

                # Liberar SWAP (Corrección del Bloque 3)
                elif info['location'] == 'SWAP' and info['frame_id'] is not None:
                    # Accedemos directo a la lista de swap del manager para liberarlo
                    # ya que memory.py no tiene un metodo 'free_swap_frame' explícito,
                    # usamos el método del objeto Frame.
                    if info['frame_id'] < len(self.memory.swap):
                        self.memory.swap[info['frame_id']].free_frame()

            del self.active_processes[pid]
            print(f"[Paging] Proceso {pid} finalizado y memoria limpiada.")
        else:
            print(f"Advertencia: El proceso {pid} no existe.")

    def print_page_table(self, pid):
        if pid in self.active_processes:
            self.active_processes[pid].show_page_table()
        else:
            print(f"Proceso {pid} no encontrado.")