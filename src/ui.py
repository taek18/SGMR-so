from simulator import OSSimulator
import os
import sys


def clear_console():
    # Limpia pantalla según windows o linux
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    print("Iniciando Sistema Operativo...")
    # Aseguramos que cargue la configuración correctamente al inicio
    try:
        sim = OSSimulator()
    except Exception as e:
        print(f"Error fatal al iniciar simulador: {e}")
        return

    while True:
        print("\n" + "=" * 40)
        print("       SIMULADOR DE MEMORIA (FIFO)")
        print("=" * 40)
        print("1. Crear nuevo proceso")
        print("2. Terminar proceso")
        print("3. Ver estado de RAM y SWAP")
        print("4. Ver tabla de páginas de un proceso")
        print("5. Ver estadísticas globales")
        print("6. Salir")
        print("-" * 40)

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            try:
                size = int(input("Tamaño del proceso (bytes): "))
                if size > 0:
                    sim.create_process(size)
                else:
                    print("El tamaño debe ser mayor a 0.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

        elif opcion == '2':
            try:
                pid = int(input("ID del Proceso a terminar: "))
                sim.terminate_process(pid)
            except ValueError:
                print("ID inválido (debe ser numérico).")

        elif opcion == '3':
            sim.show_memory_status()

        elif opcion == '4':
            try:
                pid = int(input("ID del Proceso: "))
                sim.show_page_table(pid)
            except ValueError:
                print("ID inválido.")

        elif opcion == '5':
            stats = sim.get_global_stats()
            print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
            for key, value in stats.items():
                print(f" > {key}: {value}")

        elif opcion == '6':
            print("Apagando simulador...")
            break
        else:
            print("Opción no reconocida.")

        input("\n[Presiona ENTER para continuar...]")
        clear_console()


if __name__ == "__main__":
    main()