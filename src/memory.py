from collections import deque


class Frame:
    def __init__(self, frame_id):
        self.id = frame_id  # número de marco
        self.process_id = None  # id de proceso
        self.page_number = None  # número de página de proces
        self.free = True  # libre al inicio

    # asignar página al marco
    def assign(self, process_id, page_number):
        self.process_id = process_id
        self.page_number = page_number
        self.free = False

    # liberación de marco
    def free_frame(self):
        self.process_id = None
        self.page_number = None
        self.free = True

    def __repr__(self):
        if self.free:
            return f"[Frame {self.id}: LIBRE]"
        return f"[Frame {self.id}: P{self.process_id}, Pag {self.page_number}]"


class MemoryManager:
    def __init__(self, frames_ram, frames_swap):
        self.ram = [Frame(i) for i in range(frames_ram)]
        self.swap = [Frame(i) for i in range(frames_swap)]

        # FIFO
        self.fifo_queue = deque()

    #--------------------#
    #  MÉTODOS PARA RAM  #
    #--------------------#

    def get_free_ram_frame(self):
        for frame in self.ram:
            if frame.free:
                return frame.id
        return None

    def allocate_ram(self, process_id, page_number):
        free_id = self.get_free_ram_frame()

        if free_id is not None:
            frame = self.ram[free_id]
            frame.assign(process_id, page_number)

            self.fifo_queue.append(free_id)

            return free_id, None
        else:
            return None, "NO_SPACE"

    def free_ram_frame(self, frame_id):
        frame = self.ram[frame_id]
        frame.free_frame()

        if frame_id in self.fifo_queue:
            self.fifo_queue.remove(frame_id)

    #-------------------------------#
    #  ALGORITMO DE REEMPLAZO FIFO  #
    #-------------------------------#

    def select_victim_fifo(self):
        if not self.fifo_queue:
            return None

        victim_frame_id = self.fifo_queue.popleft()
        return victim_frame_id

    # --------------------#
    #  MÉTODOS PARA SWAP  #
    # --------------------#

    def get_free_swap_frame(self):
        for frame in self.swap:
            if frame.free:
                return frame.id
        return None

    def move_ram_to_swap(self, frame_id):
        swap_id = self.get_free_swap_frame()
        if swap_id is None:
            return None, "SWAP_FULL"

        ram_frame = self.ram[frame_id]
        swap_frame = self.swap[swap_id]

        swap_frame.assign(ram_frame.process_id, ram_frame.page_number)

        ram_frame.free_frame()

        return swap_id, None

    # ----------------#
    #  VISUALIZACIÓN  #
    # ----------------#

    def print_ram(self):
        print("\n--- ESTADO DE RAM---")
        for frame in self.ram:
            print(frame)

    def print_swap(self):
        print("\n--- ESTADO DE SWAP---")
        for frame in self.swap:
            print(frame)