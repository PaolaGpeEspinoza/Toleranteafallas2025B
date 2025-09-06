import threading
import multiprocessing
import time
import random
import asyncio
import nest_asyncio

nest_asyncio.apply()

# Tarea simulada
def tarea_simulada(nombre, duracion=2, fallo_prob=0.3, tipo="I/O"):
    print(f"{nombre} iniciada | Tipo de tarea: {tipo}")
    
    if tipo == "I/O":
        time.sleep(duracion)
    elif tipo == "CPU":
        sum(i*i for i in range(10**6))
        time.sleep(0.1)
    elif tipo == "Mixto":
        time.sleep(duracion/2)
        sum(i*i for i in range(5*10**5))
    
    if random.random() < fallo_prob:
        print(f"{nombre} ha fallado ❌")
        raise Exception(f"Tarea {nombre} falló")
    
    print(f"{nombre} finalizada ✅")
    return True

# Hilos normales
def ejecutar_threads(n_tareas=5, fallo_prob=0.3, tipo="I/O"):
    resultados = []
    def worker(nombre):
        try:
            tarea_simulada(nombre, duracion=random.uniform(1,3), fallo_prob=fallo_prob, tipo=tipo)
            resultados.append(True)
        except:
            resultados.append(False)
    
    hilos = []
    for i in range(n_tareas):
        t = threading.Thread(target=worker, args=(f"Hilo-{i+1}",))
        hilos.append(t)
        t.start()
    for t in hilos:
        t.join()
    return resultados

# Hilos daemon
def ejecutar_threads_daemon(n_tareas=5, fallo_prob=0.3, tipo="I/O"):
    resultados = []
    def worker(nombre):
        try:
            tarea_simulada(nombre, duracion=random.uniform(1,3), fallo_prob=fallo_prob, tipo=tipo)
            resultados.append(True)
        except:
            resultados.append(False)
    
    hilos = []
    for i in range(n_tareas):
        t = threading.Thread(target=worker, args=(f"Daemon-{i+1}",))
        t.daemon = True
        hilos.append(t)
        t.start()
    for t in hilos:
        t.join()
    return resultados

# Procesos
def worker_proceso(nombre, fallo_prob=0.3, tipo="I/O", resultados=None):
    try:
        tarea_simulada(nombre, duracion=random.uniform(1,3), fallo_prob=fallo_prob, tipo=tipo)
        if resultados is not None:
            resultados.append(True)
    except:
        if resultados is not None:
            resultados.append(False)

def ejecutar_procesos(n_tareas=5, fallo_prob=0.3, tipo="I/O"):
    manager = multiprocessing.Manager()
    resultados = manager.list()
    
    procesos = []
    for i in range(n_tareas):
        p = multiprocessing.Process(target=worker_proceso, args=(f"Proceso-{i+1}", fallo_prob, tipo, resultados))
        procesos.append(p)
        p.start()
    for p in procesos:
        p.join()
    return list(resultados)

# Async
async def tarea_async(nombre, duracion=2, fallo_prob=0.3, tipo="I/O"):
    print(f"{nombre} iniciada | Tipo de tarea: {tipo} (Async)")
    
    if tipo == "I/O":
        await asyncio.sleep(duracion)
    elif tipo == "CPU":
        sum(i*i for i in range(10**6))
        await asyncio.sleep(0.1)
    elif tipo == "Mixto":
        await asyncio.sleep(duracion/2)
        sum(i*i for i in range(5*10**5))
    
    if random.random() < fallo_prob:
        print(f"{nombre} ha fallado ❌")
        raise Exception(f"Tarea {nombre} falló")
    
    print(f"{nombre} finalizada ✅")
    return True

async def ejecutar_async(n_tareas=5, fallo_prob=0.3, tipo="I/O"):
    tareas = []
    resultados = []
    async def wrapper(nombre):
        try:
            await tarea_async(nombre, duracion=random.uniform(1,3), fallo_prob=fallo_prob, tipo=tipo)
            resultados.append(True)
        except:
            resultados.append(False)
    
    for i in range(n_tareas):
        tareas.append(wrapper(f"Async-{i+1}"))
    
    await asyncio.gather(*tareas)
    return resultados

def ejecutar_async_safe(n_tareas=5, fallo_prob=0.3, tipo="I/O"):
    return asyncio.run(ejecutar_async(n_tareas, fallo_prob, tipo))

# Medición
def medir(func, *args):
    inicio = time.perf_counter()
    resultados = func(*args)
    fin = time.perf_counter()
    tiempo = fin - inicio
    exitos = sum(resultados)
    fallidas = len(resultados) - exitos
    return tiempo, exitos, fallidas

# Experimento con múltiples rondas
def ejecutar_experimento(n_rondas=3, n_tareas=5, fallo_prob=0.3, tipo="I/O"):
    resumen = {
        "Hilos": {"tiempo_total":0, "exitos":0, "fallos":0},
        "Hilos Daemon": {"tiempo_total":0, "exitos":0, "fallos":0},
        "Procesos": {"tiempo_total":0, "exitos":0, "fallos":0},
        "Async": {"tiempo_total":0, "exitos":0, "fallos":0}
    }
    
    for ronda in range(1, n_rondas+1):
        print(f"\n=== Ronda {ronda} | Tipo de tarea: {tipo} ===")
        
        t, e, f = medir(ejecutar_threads, n_tareas, fallo_prob, tipo)
        print(f"[Hilos] Tiempo: {t:.2f}s | Éxitos: {e} | Fallos: {f}")
        resumen["Hilos"]["tiempo_total"] += t
        resumen["Hilos"]["exitos"] += e
        resumen["Hilos"]["fallos"] += f
        
        t, e, f = medir(ejecutar_threads_daemon, n_tareas, fallo_prob, tipo)
        print(f"[Hilos Daemon] Tiempo: {t:.2f}s | Éxitos: {e} | Fallos: {f}")
        resumen["Hilos Daemon"]["tiempo_total"] += t
        resumen["Hilos Daemon"]["exitos"] += e
        resumen["Hilos Daemon"]["fallos"] += f
        
        t, e, f = medir(ejecutar_procesos, n_tareas, fallo_prob, tipo)
        print(f"[Procesos] Tiempo: {t:.2f}s | Éxitos: {e} | Fallos: {f}")
        resumen["Procesos"]["tiempo_total"] += t
        resumen["Procesos"]["exitos"] += e
        resumen["Procesos"]["fallos"] += f
        
        t, e, f = medir(ejecutar_async_safe, n_tareas, fallo_prob, tipo)
        print(f"[Async] Tiempo: {t:.2f}s | Éxitos: {e} | Fallos: {f}")
        resumen["Async"]["tiempo_total"] += t
        resumen["Async"]["exitos"] += e
        resumen["Async"]["fallos"] += f
    
    # Promedios y mejor método
    print("\n=== RESULTADOS PROMEDIO ===")
    mejor_metodo = None
    mejor_tiempo = float('inf')
    
    for metodo, datos in resumen.items():
        tiempo_prom = datos["tiempo_total"]/n_rondas
        exitos_prom = datos["exitos"]/n_rondas
        fallos_prom = datos["fallos"]/n_rondas
        print(f"{metodo}: Tiempo promedio: {tiempo_prom:.2f}s | Éxitos promedio: {exitos_prom:.2f} | Fallos promedio: {fallos_prom:.2f}")
        
        if exitos_prom > 0 and tiempo_prom < mejor_tiempo:
            mejor_tiempo = tiempo_prom
            mejor_metodo = metodo
    
    print(f"\n>> Mejor método según experimento: {mejor_metodo}")

# Función principal
def main():
    for tipo_tarea in ["I/O", "CPU", "Mixto"]:
        print(f"\n=== EXPERIMENTO TIPO {tipo_tarea} ===")
        ejecutar_experimento(n_rondas=3, n_tareas=5, fallo_prob=0.3, tipo=tipo_tarea)

if __name__ == "__main__":
    main()
