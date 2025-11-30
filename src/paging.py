class PagingSystem:
    def __init__(self, memory_manager, page_size):
        self.memory = memory_manager
        self.page_size = page_size
        # Guardamos referencia a los procesos activos {pid: objeto_proceso}
        # Esto nos servirá para acceder a sus tablas de páginas y actualizarlas.
        self.active_processes = {}

    def load_process(self, process):
        print(f"[Paging] Intentando cargar proceso {process.pid} ({process.num_pages} páginas) en RAM...")

        # Guardamos el proceso en nuestro registro
        self.active_processes[process.pid] = process

        # Intentamos asignar marcos de RAM para cada página
        for i in range(process.num_pages):
            # Solicitamos memoria al MemoryManager
            frame_id, error = self.memory.allocate_ram(process.pid, i)

            if error == "NO_SPACE":
                # AQUÍ irá la lógica FIFO en el siguiente paso.
                # Por ahora, simplemente reportamos el error y fallamos.
                print(f"   [!] RAM llena al intentar cargar página {i}. Se requiere Swapping.")
                return False

            # Si asignó bien, actualizamos la tabla del proceso (Vicente's module)
            # location='RAM' indica que está en memoria física
            process.update_page_status(page_number=i, frame_id=frame_id, location='RAM')

        print(f"[Paging] Proceso {process.pid} cargado exitosamente en RAM.")
        return True

    def unload_process(self, pid):
        """ Libera los marcos de RAM ocupados por el proceso y lo saca del registro. """
        if pid in self.active_processes:
            process = self.active_processes[pid]

            # Recorremos la tabla de páginas del proceso para liberar marcos
            for page_num, info in process.page_table.items():
                if info['location'] == 'RAM' and info['frame_id'] is not None:
                    self.memory.free_ram_frame(info['frame_id'])

            del self.active_processes[pid]
            print(f"[Paging] Recursos del proceso {pid} liberados.")
        else:
            print(f"Advertencia: Intentando descargar proceso {pid} que no existe en Paging.")

    def print_page_table(self, pid):
        """ Muestra la tabla de páginas usando el método del propio proceso. """
        if pid in self.active_processes:
            self.active_processes[pid].show_page_table()
        else:
            print(f"Proceso {pid} no encontrado.")