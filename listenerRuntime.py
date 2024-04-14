import schedule
import time

def tarea():
    print("¡Esta es tu tarea ejecutándose cada minuto!")

# Programa la tarea para que se ejecute cada minuto
schedule.every(1).minutes.do(tarea)

# Ejecuta el ciclo de planificación
while True:
    schedule.run_pending()
    time.sleep(1)  # Pausa de 1 segundo para evitar consumir demasiados recursos
