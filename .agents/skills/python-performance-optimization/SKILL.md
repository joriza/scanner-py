# Python Performance Optimization Skill

## Descripción
Esta habilidad proporciona conocimientos y técnicas para optimizar el rendimiento de aplicaciones Python. Incluye desde la identificación de cuellos de botella hasta la implementación de optimizaciones avanzadas.

## Requisitos Previos
- Python 3.8 o superior instalado
- Conocimientos básicos de Python
- Familiaridad con conceptos de programación orientada a objetos

## Herramientas de Perfilado

### cProfile
```bash
# Ejecutar script con cProfile
python -m cProfile -o profile_output.py script.py

# Visualizar resultados con pstats
python -m pstats profile_output.py
```

### timeit
```python
import timeit

# Medir tiempo de ejecución de una función
timeit.timeit('funcion()', setup='from __main__ import funcion', number=1000)

# Medir tiempo en línea de comandos
python -m timeit 'funcion()'
```

### line_profiler
```bash
# Instalar
pip install line_profiler

# Decorar función para perfilado
@profile
def funcion():
    # código

# Ejecutar
kernprof -l -v script.py
```

### memory_profiler
```bash
# Instalar
pip install memory_profiler

# Decorar función para perfilado de memoria
@profile
def funcion():
    # código

# Ejecutar
python -m memory_profiler script.py
```

## Optimizaciones de Código

### Uso de Generadores
```python
# Ineficiente: crea lista completa en memoria
def procesar_lista(lista):
    return [x * 2 for x in lista]

# Eficiente: genera valores bajo demanda
def procesar_generador(lista):
    for x in lista:
        yield x * 2
```

### Comprensiones vs Bucles
```python
# Ineficiente
resultado = []
for x in range(1000):
    resultado.append(x * 2)

# Eficiente
resultado = [x * 2 for x in range(1000)]
```

### Uso de Sets para Búsqueda
```python
# Ineficiente: O(n)
if elemento in lista:
    # código

# Eficiente: O(1)
if elemento in set(lista):
    # código
```

### Evitar Concatenación de Strings en Bucles
```python
# Ineficiente
resultado = ""
for x in range(1000):
    resultado += str(x)

# Eficiente
resultado = "".join(str(x) for x in range(1000))
```

## Optimizaciones de Estructuras de Datos

### Uso de __slots__
```python
class Persona:
    __slots__ = ['nombre', 'edad']
    
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
```

### Uso de namedtuples
```python
from collections import namedtuple

Persona = namedtuple('Persona', ['nombre', 'edad'])
p = Persona('Juan', 30)
```

### Uso de dataclasses (Python 3.7+)
```python
from dataclasses import dataclass

@dataclass
class Persona:
    nombre: str
    edad: int
```

## Optimizaciones de Algoritmos

### Uso de Algoritmos Eficientes
```python
# Ineficiente: O(n²)
def buscar_duplicados(lista):
    for i, x in enumerate(lista):
        if x in lista[i+1:]:
            return True
    return False

# Eficiente: O(n)
def buscar_duplicados(lista):
    return len(lista) != len(set(lista))
```

### Uso de Memoización
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Optimizaciones de I/O

### Uso de Buffered I/O
```python
# Ineficiente
with open('archivo.txt', 'r') as f:
    for line in f:
        process(line)

# Eficiente
with open('archivo.txt', 'r', buffering=8192) as f:
    for line in f:
        process(line)
```

### Uso de Async I/O (Python 3.5+)
```python
import asyncio

async def procesar_archivo(nombre_archivo):
    async with aiofiles.open(nombre_archivo, 'r') as f:
        async for line in f:
            process(line)
```

## Uso de Extensiones C/C++

### Cython
```python
# archivo.pyx
def suma_rapida(int a, int b):
    return a + b
```

### Numba
```python
from numba import jit

@jit(nopython=True)
def suma_rapida(a, b):
    return a + b
```

## Paralelización

### multiprocessing
```python
from multiprocessing import Pool

def procesar_dato(dato):
    # procesamiento
    return resultado

with Pool(processes=4) as pool:
    resultados = pool.map(procesar_dato, datos)
```

### concurrent.futures
```python
from concurrent.futures import ThreadPoolExecutor

def procesar_dato(dato):
    # procesamiento
    return resultado

with ThreadPoolExecutor(max_workers=4) as executor:
    resultados = list(executor.map(procesar_dato, datos))
```

## Mejores Prácticas

### Evitar Premature Optimization
- Primero haz que el código funcione correctamente
- Luego identifica los cuellos de botella con herramientas de perfilado
- Solo optimiza las partes que realmente afectan el rendimiento

### Medir, No Adivinar
- Siempre usa herramientas de medición antes y después de optimizar
- Documenta las mejoras de rendimiento obtenidas

### Mantenibilidad vs Rendimiento
- No sacrificar la legibilidad del código por micro-optimizaciones
- Prioriza algoritmos eficientes sobre trucos de lenguaje

## Recursos Adicionales
- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [Profiling Python Code](https://docs.python.org/3/library/profile.html)
- [Cython Documentation](https://cython.readthedocs.io/)
- [Numba Documentation](https://numba.readthedocs.io/)
