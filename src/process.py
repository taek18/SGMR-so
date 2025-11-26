import math

class process():
    def __init__(self, pid, size, page_size):
        self.pid=pid #identificador del proceso
        self.size=size #tamaño del proceso en bytes
        self.page_size=page_size #tamaño de una pagina en bytes

        #cuantas pagina requiere
        self.num_pages=math.ceil(size/page_size)

        #tabla de paginas
        self.page_table={}
        self.init_page_table()

    def init_page_table(self):
        for i in range(self.num_pages):
            self.page_table[i]={
                'frame_id': None,
                'location': None,  #ram-swap o none
                'present': False  #true si esta en ram
            }

    def update_page_status(self, page_number, frame_id, location):
        if page_number in self.page_table:
            self.page_table[page_number]['frame_id']=frame_id
            self.page_table[page_number]['location']=location

            # present es True solo si esta en RAM fisica
            self.page_table[page_number]['present']=(location=='RAM')
        else:
            print(f"Error: La pagina {page_number} no existe en el proceso {self.pid}")

    def get_total_pages(self):
        return self.num_pages

    def show_page_table(self):

        #mostrar la tabla de paginas formateada
        print(f"\n--- Tabla de Paginas: Proceso ID {self.pid} ---")
        print(f"Tamaño: {self.size} KB | Total Paginas: {self.num_pages}")
        print("-"*55)
        print(f"{'Pagina Logica':<15} | {'Ubicacion':<10} | {'Marco Fisico':<12} | {'Presente (RAM)':<15}")
        print("-" *55)

        for page, info in self.page_table.items():
            loc=info['location'] if info['location'] else "Sin cargar"
            fid=info['frame_id'] if info['frame_id'] is not None else "-"
            present="Si" if info['present'] else "No"

            print(f"{page:<15} | {loc:<10} | {fid:<12} | {present:<15}")
        print("-"*55)

    def __repr__(self):
        return f"<Proceso {self.pid}: {self.size}KB ({self.num_pages} pags)>"

# CODIGO DE PRUEBA si requiere cambios
"""
if __name__ == "__main__":
    #Supongamos que el tamaño de pagina es 1024 KB
    PAGE_SIZE_TEST = 1024

    #crear proceso (opcion 1 del menu)
    #proceso de 5000 KB. deberia requerir 5 paginas (5000/1024=4.88->5)
    p1 = process(pid=1, size=5000, page_size=PAGE_SIZE_TEST)

    print(f"Proceso creado: {p1}")
    print(f"Páginas calculadas: {p1.get_total_pages()}")

    print("\nSimulando carga de paginas...")
    p1.update_page_status(0, frame_id=10, location='RAM')
    p1.update_page_status(1, frame_id=11, location='RAM')
    p1.update_page_status(2, frame_id=5, location='SWAP')

    #mostrar tabla de paginas (opcion 5 del menu)
    p1.show_page_table()"""