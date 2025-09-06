# Actividad 4 - Scaling Distributed Python Applications

## 📌 Descripción
Este proyecto forma parte de la materia **Programación Tolerante a Fallas**.  
El objetivo es **comparar diferentes modelos de concurrencia en Python** para analizar en qué tipo de tareas funcionan mejor.  

Se implementaron los siguientes enfoques:
- **Hilos (Threads)**
- **Hilos Daemon (Daemon Threads)**
- **Procesos (Multiprocessing)**
- **Programación Asíncrona (Asyncio)**

Cada modelo se somete a diferentes tipos de tareas (I/O, CPU y Mixto) para observar:
- Tiempo total de ejecución
- Número de tareas exitosas
- Número de tareas fallidas

---
📊 Resultados esperados

Al correr el programa se mostrarán en consola varias rondas de prueba.
Ejemplo de salida:

=== Ronda 1 | Tipo de tarea: I/O ===
Hilo-1 iniciada | Tipo de tarea: I/O
Hilo-2 iniciada | Tipo de tarea: I/O
Hilo-3 iniciada | Tipo de tarea: I/O
Hilo-4 iniciada | Tipo de tarea: I/O
Hilo-5 iniciada | Tipo de tarea: I/O
Hilo-1 finalizada ✅
Hilo-3 ha fallado ❌
...
[Hilos] Tiempo: 2.80s | Éxitos: 3 | Fallos: 2
[Procesos] Tiempo: 3.07s | Éxitos: 5 | Fallos: 0
[Daemon Threads] Tiempo: 2.95s | Éxitos: 4 | Fallos: 1
[Asyncio] Tiempo: 2.50s | Éxitos: 5 | Fallos: 0

📖 Observaciones

- Los hilos suelen rendir mejor en tareas I/O (espera de archivos, red, etc.).

- Los procesos aprovechan varios núcleos de la CPU, siendo más eficientes en tareas CPU-intensivas.

- Los hilos daemon permiten liberar recursos automáticamente al terminar el programa.

- La programación asíncrona es muy eficiente en I/O pero más difícil de implementar en tareas CPU-bound.



