import logging

# Configurar logging para registrar errores en un archivo
logging.basicConfig(filename="verificacionerrores.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def validar_contraseña(password):
    """Valida si la contraseña cumple con los requisitos mínimos."""
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not any(c.isupper() for c in password):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
    if not any(c.isdigit() for c in password):
        raise ValueError("La contraseña debe contener al menos un número.")
    return "Contraseña válida"

def dividir_numeros(a, b):
    """Maneja errores de división por cero."""
    try:
        return a / b
    except ZeroDivisionError:
        logging.error("Intento de división por cero")
        return "Error: No se puede dividir por cero."
    
#Programa principal
try:
    # Solicitar contraseña al usuario
    contrasena = input("Ingresa tu contraseña: ")
    print(validar_contraseña(contrasena))
    
    # Solicitar dos números para dividir
    num1 = int(input("Ingresa el primer número: "))
    num2 = int(input("Ingresa el segundo número: "))
    
    resultado = dividir_numeros(num1, num2)
    print(f"Resultado de la división: {resultado}")

except ValueError as e:
    logging.error(f"Error de valor: {e}")
    print(f"Error: {e}")

except Exception as e:
    logging.error(f"Error inesperado: {e}")
    print(f"Ocurrió un error inesperado: {e}")

finally:
    print("Proceso finalizado")
