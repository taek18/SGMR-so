class PagingSystem:
    def __init__(self, memory_manager, page_size):
        self.memory = memory_manager
        self.page_size = page_size
        self.active_processes = {}

    def load_process(self, process):
        print(f"[Paging] Intentando cargar proceso {process.pid} ({process.num_pages} páginas)...")
        self.active_processes[process.pid] = process

        for i in range(process.num_pages):
            # 1. Intentar asignar en RAM
            frame_id, error = self.memory.allocate_ram(process.pid, i)

            if error == "NO_SPACE":
                print(f"   [!] RAM llena al intentar cargar página {i}. Ejecutando reemplazo FIFO...")

                # A) Seleccionar víctima (FIFO)
                victim_frame_id = self.memory.select_victim_fifo()
                if victim_frame_id is None:
                    print("Error crítico: No se pudo seleccionar víctima.")
                    return False

                # B) Identificar de quién es ese marco para actualizar su tabla
                # Accedemos al marco en RAM para ver el PID y Página antes de moverlo
                victim_frame = self.memory.ram[victim_frame_id]
                victim_pid = victim_frame.process_id
                victim_page_num = victim_frame.page_number

                # C) Mover a Swap
                swap_id, swap_err = self.memory.move_ram_to_swap(victim_frame_id)
                if swap_err:
                    print(f"Error fatal: Swap lleno ({swap_err}). No se puede cargar proceso.")
                    return False

                print(
                    f"      > Víctima liberada: Marco {victim_frame_id} (Proc {victim_pid}, Pag {victim_page_num}) movido a Swap {swap_id}")

                # D) Actualizar la tabla de páginas del proceso víctima
                if victim_pid in self.active_processes:
                    victim_proc = self.active_processes[victim_pid]
                    # Le decimos: "Tu página ya no está en RAM, ahora está en SWAP"
                    victim_proc.update_page_status(victim_page_num, swap_id, 'SWAP')

                # E) Ahora que liberamos espacio, asignamos el marco al proceso actual
                frame_id, error = self.memory.allocate_ram(process.pid, i)
                if error:
                    print(f"Error al reasignar marco liberado: {error}")
                    return False

            # Si llegamos aquí, tenemos un frame_id válido (sea directo o post-swap)
            process.update_page_status(i, frame_id, 'RAM')

        print(f"[Paging] Proceso {process.pid} cargado exitosamente.")
        return True

    def unload_process(self, pid):
        if pid in self.active_processes:
            process = self.active_processes[pid]
            # Liberar marcos (RAM y SWAP)
            # Nota: Por ahora solo liberamos RAM para cumplir el requisito básico,
            # pero idealmente deberíamos liberar swap también si el proceso muere.
            for page_num, info in process.page_table.items():
                if info['location'] == 'RAM' and info['frame_id'] is not None:
                    self.memory.free_ram_frame(info['frame_id'])

            del self.active_processes[pid]
            print(f"[Paging] Proceso {pid} terminado y recursos liberados.")
        else:
            print(f"Advertencia: Proceso {pid} no encontrado.")

    def print_page_table(self, pid):
        if pid in self.active_processes:
            self.active_processes[pid].show_page_table()
        else:
            print(f"Proceso {pid} no encontrado.")