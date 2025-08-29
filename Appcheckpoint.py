import pickle
import os
import time
from datetime import datetime

ARCHIVO = "estado.pkl"

def guardar_estado(estado: dict):
    """
    Guarda el estado actual en un archivo binario usando pickle.
    Incluye el valor del contador y la fecha/hora del último guardado.
    """
    with open(ARCHIVO, "wb") as f:
        pickle.dump(estado, f)

def cargar_estado() -> dict:
    """
    Carga el estado desde disco si existe.
    Si no existe, inicia desde cero con fecha actual.
    """
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "rb") as f:
            return pickle.load(f)
    return {"contador": 0, "ultima_actualizacion": str(datetime.now())}

def main():
    datos = cargar_estado()
    contador = datos["contador"]

    print(" Estado cargado:")
    print(f"   → Contador previo: {contador}")
    print(f"   → Última actualización: {datos['ultima_actualizacion']}")

    continuar = True
    while continuar:
        try:
            contador += 1
            print(f"Contador actual: {contador}")

            # Guardado automático cada 4 ciclos
            if contador % 4 == 0:
                estado = {
                    "contador": contador,
                    "ultima_actualizacion": str(datetime.now())
                }
                guardar_estado(estado)
                print(f" Estado guardado a las {estado['ultima_actualizacion']}")

            time.sleep(1)

        except KeyboardInterrupt:
            print("\n Interrupción detectada. Guardando antes de salir...")
            estado = {
                "contador": contador,
                "ultima_actualizacion": str(datetime.now())
            }
            guardar_estado(estado)
            print(f" Estado final almacenado ({estado['ultima_actualizacion']}).")
            continuar = False

if __name__ == "__main__":
    main()
