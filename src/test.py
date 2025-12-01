import config_loader
from simulator import OSSimulator


def separator(title):
    print("\n" + "=" * 60)
    print(f"TEST: {title}")
    print("=" * 60)


def test_1_basic_process_load():
    separator("1) Carga básica de procesos")

    sim = OSSimulator()

    sim.create_process(200)
    sim.create_process(300)

    stats = sim.get_global_stats()
    print("\nEstadísticas:", stats)
    assert isinstance(stats["Fallos de Página"], int)


def test_2_force_swapping():
    separator("2) Forzar swapping llenando RAM")

    sim = OSSimulator()

    # RAM = 8 frames → este proceso fuerza swapping
    sim.create_process(3000)  # ≈ 12 páginas

    print("\nVer estado final de RAM:")
    sim.show_memory_status()

    stats = sim.get_global_stats()
    print("\nEstadísticas:", stats)

    assert sim.paging.page_faults > 0, "Debe haber fallos de página al activar FIFO"


def test_3_page_table_integrity():
    separator("3) Integridad de tabla de páginas")

    sim = OSSimulator()

    psize = 700
    sim.create_process(psize)

    pid = 1
    print("\nTabla de páginas del proceso:")
    sim.show_page_table(pid)

    proc = sim.processes[pid]

    assert len(proc.page_table) == proc.num_pages
    assert proc.state in ["active", "partially_swapped", "swapped"]


def test_4_swap_in_operation():
    separator("4) Test explícito de swap-in")

    sim = OSSimulator()

    sim.create_process(1500)  # 6 páginas
    pid = 1
    proc = sim.processes[pid]

    swap_pages = [
        p for p, info in proc.page_table.items()
        if info["location"] == "SWAP"
    ]

    if not swap_pages:
        print("No hubo páginas en swap. Cambiar tamaños para test.")
        return

    page_to_bring = swap_pages[0]
    print(f"\nIntentando swap-in de página {page_to_bring} del proceso {pid}...")
    result = sim.paging.swap_in(pid, page_to_bring)

    assert result is True, "swap_in debe funcionar"
    assert proc.page_table[page_to_bring]["location"] == "RAM"
    print("swap_in exitoso.")


def test_5_process_termination():
    separator("5) Terminación de proceso y limpieza")

    sim = OSSimulator()

    sim.create_process(900)  # varias páginas
    sim.create_process(1200)

    print("\nEliminando proceso 1...")
    sim.terminate_process(1)

    assert 1 not in sim.processes
    print("Proceso eliminado correctamente.")

    print("\nEstado de RAM/SWAP:")
    sim.show_memory_status()


# -----------------------------
# EJECUCIÓN DIRECTA DE TESTS
# -----------------------------
if __name__ == "__main__":
    separator("INICIANDO PRUEBAS DEL SISTEMA OPERATIVO")

    test_1_basic_process_load()
    test_2_force_swapping()
    test_3_page_table_integrity()
    test_4_swap_in_operation()
    test_5_process_termination()

    print("\n✔ TODOS LOS TESTS SE EJECUTARON (revisa consola para ver detalles).")
