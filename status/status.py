import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
import psutil
import threading
import time

LOG_FILE = "monitor_procesos.txt"
running = True


def get_process(app_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] and app_name.lower() in process.info['name'].lower():
            return process
    return None


def monitor_process():
    """Hilo que monitorea el proceso"""
    while running:
        app_name = entry.get()

        if app_name:
            process = get_process(app_name)

            if process:
                try:
                    cpu = process.cpu_percent(interval=0.5)
                    mem = process.memory_info().rss / 1024 / 1024

                    update_ui(
                        True,
                        process.pid,
                        cpu,
                        mem
                    )

                    log_data(process.pid, cpu, mem)

                except psutil.NoSuchProcess:
                    update_ui(False)

            else:
                update_ui(False)

        time.sleep(2)


def update_ui(found, pid=None, cpu=None, mem=None):
    """Actualización segura de la UI"""
    def callback():
        if found:
            status_label.config(text="✅ Proceso activo", fg="green")
            pid_label.config(text=f"PID: {pid}")
            cpu_label.config(text=f"CPU: {cpu:.2f}%")
            mem_label.config(text=f"Memoria: {mem:.2f} MB")

            cpu_bar['value'] = min(cpu, 100)
            mem_bar['value'] = min(mem, 1000)
        else:
            status_label.config(text="❌ Proceso no encontrado", fg="red")
            pid_label.config(text="PID: -")
            cpu_label.config(text="CPU: -")
            mem_label.config(text="Memoria: -")
            cpu_bar['value'] = 0
            mem_bar['value'] = 0

    window.after(0, callback)


def kill_process():
    app_name = entry.get()
    process = get_process(app_name)

    if process:
        confirm = messagebox.askyesno(
            "Confirmar",
            f"¿Finalizar el proceso PID {process.pid}?"
        )
        if confirm:
            process.terminate()
            messagebox.showinfo("Finalizado", "Proceso terminado.")
    else:
        messagebox.showerror("Error", "Proceso no encontrado")


def log_data(pid, cpu, mem):
    with open(LOG_FILE, "a") as f:
        f.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"PID: {pid} | CPU: {cpu:.2f}% | MEM: {mem:.2f} MB\n"
        )


def on_close():
    global running
    running = False
    window.destroy()


# ---------- GUI ----------
window = tk.Tk()
window.title("Monitor de Procesos con Hilos")
window.geometry("430x420")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", on_close)

tk.Label(
    window,
    text="Monitor de Procesos (Threading)",
    font=("Arial", 14, "bold")
).pack(pady=10)

tk.Label(window, text="Nombre del proceso:").pack()
entry = tk.Entry(window, width=30)
entry.pack(pady=5)
entry.insert(0, "whatsapp.exe")

status_label = tk.Label(window, text="", font=("Arial", 11))
status_label.pack(pady=5)

pid_label = tk.Label(window, text="PID: -")
pid_label.pack()

cpu_label = tk.Label(window, text="CPU: -")
cpu_label.pack()
cpu_bar = Progressbar(window, length=280, maximum=100)
cpu_bar.pack(pady=5)

mem_label = tk.Label(window, text="Memoria: -")
mem_label.pack()
mem_bar = Progressbar(window, length=280, maximum=1000)
mem_bar.pack(pady=5)

tk.Button(
    window,
    text="❌ Finalizar Proceso",
    command=kill_process,
    bg="#ff5f5f"
).pack(pady=15)


# ---------- HILO ----------
thread = threading.Thread(target=monitor_process, daemon=True)
thread.start()

window.mainloop()
