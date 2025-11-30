import configparser
import os
import sys

def load_config(filename = 'config.ini'):
    config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))

    if not os.path.exists(filename):
        print(f"Error: El archivo {filename} no existe.")
        sys.exit(1)

    files = config.read(filename)
    if len(files) == 0:
        print(f"Error: No se pudo leer el archivo {filename}.")
        sys.exit(1)

    if 'MEMORY' not in config:
        print("Error: el archivo config.ini no contiene la sección [MEMORY].")
        sys.exit(1)

    section = config['MEMORY']
    required_keys = ['ram_size', 'swap_size', 'page_size']

    for key in required_keys:
        if key not in section:
            print(f"Error: no se encontro la clave '{key}' dentro de [MEMORY].")
            sys.exit(1)

    try:
        ram_size = int(section['ram_size'])
        swap_size = int(section['swap_size'])
        page_size = int(section['page_size'])
    except ValueError:
        print("Error: los valores de [MEMORY] deben ser númericos enteros.")
        sys.exit(1)

    if ram_size <= 0 or swap_size <= 0 or page_size <= 0:
        print("Error: todos los valores deben ser mayores a cero.")
        sys.exit(1)

    if ram_size % page_size != 0:
        print("Error: RAM no es múltiplo exacto…")
        sys.exit(1)
    if swap_size % page_size != 0:
        print("Error: RAM no es múltiplo exacto…")
        sys.exit(1)

    frames_ram = ram_size // page_size
    frames_swap = swap_size // page_size

    cfg = {
        "ram_size": ram_size,
        "swap_size": swap_size,
        "page_size": page_size,
        "frames_ram": frames_ram,
        "frames_swap": frames_swap
    }

    return cfg


if __name__ == '__main__':
    config = load_config()
    print("CONFIG LOADED:", config)