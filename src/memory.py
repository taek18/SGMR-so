class Frame:
    def __init__(self, frame_id):
        self.id = frame_id          # número de marco
        self.process_id = None      # id de proceso
        self.page_number = None     # número de página de proces
        self.free = True            # libre al inicio

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
