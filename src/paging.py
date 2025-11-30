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
        self.page_faults = 0

    def load_process(self, process):
        """
        Carga un proceso en memoria. Si la RAM está llena, aplica FIFO.
        """
        print(f"[Paging] Cargando proceso {process.pid} ({process.num_pages} pags)...")
        # Registrar proceso en active_processes
        self.active_processes[process.pid] = process

        for i in range(process.num_pages):
            # 1. Intentar asignar en RAM
            frame_id, error = self.memory.allocate_ram(process.pid, i)

            if error == "NO_SPACE":
                # Contar esto como un page fault (se requiere swapping)
                self.page_faults += 1

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

                print(
                    f"      > SwapOut: Marco {victim_frame_id} (P{victim_pid}, Pag {victim_page_num}) -> Swap {swap_id}")

                # D) Actualizar tabla de páginas de la víctima (si existe)
                if victim_pid in self.active_processes:
                    self.active_processes[victim_pid].update_page_status(victim_page_num, swap_id, 'SWAP')

                # E) Asignar el marco liberado al proceso actual
                frame_id, error = self.memory.allocate_ram(process.pid, i)
                if error:
                    # si falla de nuevo, abortamos
                    print(f"Error: no se pudo asignar marco tras swap-out (proc {process.pid}, pag {i}).")
                    return False

            # Si llegamos aquí, frame_id es válido y la página queda en RAM
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

            # marcar proceso como terminado (por si algún módulo lo consulta antes de borrarlo)
            process.state = "terminated"

            # limpiar la estructura y eliminar del registro
            del self.active_processes[pid]
            print(f"[Paging] Proceso {pid} finalizado y memoria limpiada.")
        else:
            print(f"Advertencia: El proceso {pid} no existe.")

    def swap_in(self, pid, page_number):
        """
        Trae una página desde SWAP a RAM (swap-in).
        Retorna True si tuvo éxito, False si falló.
        """
        if pid not in self.active_processes:
            print(f"[swap_in] Proceso {pid} no está registrado.")
            return False

        proc = self.active_processes[pid]
        entry = proc.page_table.get(page_number)
        if entry is None:
            print(f"[swap_in] Página {page_number} fuera de rango para P{pid}.")
            return False

        # Si ya está en RAM, nada que hacer
        if entry['location'] == 'RAM' and entry['frame_id'] is not None:
            return True

        # Debe estar en swap (si no, es un caso lógico)
        swap_slot = entry.get('frame_id')
        if swap_slot is None:
            print(f"[swap_in] La página {page_number} de P{pid} no está en SWAP.")
            return False

        # Intentar asignar un marco en RAM
        frame_id, err = self.memory.allocate_ram(pid, page_number)
        if err == "NO_SPACE":
            # page fault por swap-in: contar y expulsar víctima
            self.page_faults += 1
            victim = self.memory.select_victim_fifo()
            if victim is None:
                print("[swap_in] No se pudo seleccionar víctima para swap-in.")
                return False

            victim_frame = self.memory.ram[victim]
            victim_pid = victim_frame.process_id
            victim_page = victim_frame.page_number

            # Mover víctima a swap
            new_swap_id, swap_err = self.memory.move_ram_to_swap(victim)
            if swap_err:
                print("[swap_in] Swap lleno al intentar swap-in.")
                return False

            # Actualizar tabla de la víctima
            if victim_pid in self.active_processes:
                self.active_processes[victim_pid].update_page_status(victim_page, new_swap_id, 'SWAP')

            # Reintentar asignación
            frame_id, err = self.memory.allocate_ram(pid, page_number)
            if err:
                print("[swap_in] Error: no se pudo asignar marco tras swap-out.")
                return False

        # Ahora tenemos frame_id en RAM; liberar la entrada en swap
        # Liberar el marco en swap (si existe)
        if swap_slot < len(self.memory.swap):
            self.memory.swap[swap_slot].free_frame()

        # Actualizar tabla del proceso
        proc.update_page_status(page_number, frame_id, 'RAM')

        # Contar el swap-in como un page fault también (opcional, pero usual)
        self.page_faults += 1

        print(f"[swap_in] Página {page_number} de P{pid} traída de Swap {swap_slot} a RAM marco {frame_id}.")
        return True

    def print_page_table(self, pid):
        if pid in self.active_processes:
            self.active_processes[pid].show_page_table()
        else:
            print(f"Proceso {pid} no encontrado.")