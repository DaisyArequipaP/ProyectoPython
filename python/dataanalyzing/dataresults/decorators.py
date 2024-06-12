import os
import time
from functools import wraps

# Decorador para manejo de excepciones
def manejar_excepciones(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error en {func.__name__}: {e}")
    return wrapper

# Decorador para crear directorios
def crear_directorio_si_no_existe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        output_dir = args[1]  # Asumimos que el segundo argumento es output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return func(*args, **kwargs)
    return wrapper

# Decorador para medir tiempo de ejecución
def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {fin - inicio:.2f} segundos")
        return resultado
    return wrapper
