```
::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::                                                    ::
::                                                    ::
::       _______.  _______ .___  ___. .______         ::
::      /       | /  _____||   \/   | |   _  \        ::
::     |   (----`|  |  __  |  \  /  | |  |_)  |       ::
::      \   \    |  | |_ | |  |\/|  | |      /        ::
::  .----)   |   |  |__| | |  |  |  | |  |\  \----.   ::
::  |_______/     \______| |__|  |__| | _| `._____|   ::
::                                                    ::
::                                                    ::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::
```

# Simulador de Gestor de Memoria RAM — SGMR

### Integrantes de equipo:
Kim Martínez Taesoo  
Guzman García Lizbeth Neri  
Chavarria Uribe Leo  
Vicente Bautista Roberto Nicolas  
Zertuche Zamora Sergio Gabriel  

## Curso
### Sistemas Operativos — 6to Semestre 
#### Dr. Muñoz Quintero Dante Adolfo
##### Universidad Autónoma de Tamaulipas.



## ! Instrucciones de ejecución del simulador !

Este proyecto está desarrollado en **Python 3**, por lo que no requiere compilación.

### ! Requisitos previos !

Asegúrate de tener instalado:

- Python 3.8 o superior  
- IDE de tu elección
### ! Configuración inicial !

Antes de ejecutar el simulador, revisa el archivo **config.ini**, el cual define:

```ini
[MEMORY]
ram_size = 2048
swap_size = 4096
page_size = 256
```

Estos valores representan:  
  * ram_size: tamaño total de la memoria física simulada (RAM)  
  * swap_size: tamaño total del área de intercambio (SWAP)  
  * page_size: tamaño de página / marco  

El simulador calculará automáticamente el número de marcos disponibles para RAM y SWAP.  

### ! Ejecutar el simulador !  
Para iniciar la interfaz del sistema, escribe en consola:  
```ini
python3 ui.py
```

Esto abrirá el menú interactivo que permite:  
1. Crear procesos  
2. Terminar procesos  
3. Ver el estado de RAM y SWAP  
4. Mostrar tablas de páginas  
5. Consultar estadísticas como fallos de página  
6. Salir del simulador  

#### Para ejecutar pruebas automáticas (opcional):
Usa:  
```ini
python3 test.py
```

Con esto puedes verificar el funcionamiento completo del sistema de memoria.  

## ! Diseño del Simulador !  
El simulador está organizado en módulos independientes, representando los componentes reales de un sistema operativo:  

config_loader.py → Carga de parámetros del sistema  
memory.py → Gestión de RAM / SWAP y FIFO  
process.py → Representación de procesos y sus tablas de página  
paging.py → Sistema de paginación, swapping y page faults  
simulator.py → Capa central que integra todos los módulos  
ui.py → Interfaz de usuario tipo CLI  

### ! Estructuras de datos utilizadas !  
#### 1. Memoria RAM y SWAP  
Ambas memorias están modeladas como **listas de objetos Frame**:
```python
self.ram = [Frame(i) for i in range(frames_ram)]
self.swap = [Frame(i) for i in range(frames_swap)]
```

Cada Frame contiene:
- process_id
- page_number
- free (bandera para marco libre u ocupado
  
Esta estructura permite:
- Acceso directo O(1)
- Iteración sencilla para buscar marcos libres
- Visualización clara del estado de la memoria

#### 2. Tabla de páginas de cada proceso  
Cada proceso mantiene un diccionario que representa su tabla de páginas:  
```python
self.page_table = {
    page_number: {
        'frame_id': int | None,
        'location': 'RAM' | 'SWAP' | None,
        'present': True | False
    }
}
```

#### 3. Algoritmo de reemplazo de páginas 
El simulador implementa FIFO (First-In, First-Out).  
Se utiliza una cola (collections.deque) para registrar qué marcos entraron primero en RAM:
```python
self.fifo_queue = deque()
```

Cuando RAM está llena:
1. Se toma el marco al frente de la cola (el más antiguo)
2. Se mueve esa página a SWAP
3. La entrada correspondiente en la tabla de páginas del proceso víctima se actualiza
4. Se asigna el marco liberado al nuevo proceso
