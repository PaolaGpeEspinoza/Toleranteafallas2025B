import requests
from datetime import datetime
import csv
from prefect import task, flow

PRECIO_OBJETIVO = 18.0
URL = "https://api.exchangerate-api.com/v4/latest/USD"
CSV_FILE = "historial_tipo_cambio.csv"

@task
def obtener_tipo_cambio():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data["rates"]["MXN"]
    else:
        return None

@task
def evaluar_tipo_cambio(valor):
    if valor is not None:
        if valor <= PRECIO_OBJETIVO:
            return "BARATO"
        else:
            return "CARO"
    return "ERROR"

@task
def mostrar_alerta(valor, estado):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if estado == "BARATO":
        print(f"[{ahora}] ALERTA: El dólar está barato (${valor} MXN). ¡Buen momento para comprar!")
    elif estado == "CARO":
        print(f"[{ahora}] El dólar sigue caro (${valor} MXN). Mejor esperar.")
    else:
        print(f"[{ahora}] No se pudo obtener el tipo de cambio.")

@task
def guardar_historial(valor):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ahora, valor])
    print(f"📊 Guardado en historial: {valor} MXN")

@flow
def flujo_tipo_cambio_mejorado():
    valor = obtener_tipo_cambio()
    if valor is not None:
        estado = evaluar_tipo_cambio(valor)
        mostrar_alerta(valor, estado)
        guardar_historial(valor)

if __name__ == "__main__":
    flujo_tipo_cambio_mejorado()

