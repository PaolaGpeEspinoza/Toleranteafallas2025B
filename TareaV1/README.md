# Proyecto V1: Clasificador de Correos con N8N y MCP

## Descripción

Este proyecto simula un sistema de clasificación de correos electrónicos utilizando **N8N** para la automatización de flujos y un **LLM (ChatGPT)** a través de MCP para análisis de contenido. La idea principal es aprender a usar estas herramientas y simular un flujo de trabajo real, donde los correos se clasifican por **prioridad** y **categoría**.

---

## Flujo de Trabajo en N8N

### 1. Nodo Trigger

Dispara el flujo automáticamente para simular la llegada de correos electrónicos.



---

### 2. Nodo Set

Se configuran los correos simulados en formato JSON.



Ejemplo de correos simulados:

```json
[
  {
    "from": "gerente@empresa.com",
    "subject": "Reunión urgente sobre el proyecto",
    "body": "Necesitamos revisar los avances del proyecto hoy a las 5 pm."
  },
  {
    "from": "ventas@tiendaonline.com",
    "subject": "Promoción exclusiva: 50% de descuento",
    "body": "Aprovecha nuestras ofertas por tiempo limitado."
  },
  {
    "from": "rh@empresa.com",
    "subject": "Pago de nómina correspondiente a octubre",
    "body": "Tu pago ha sido procesado correctamente."
  }
]
```

---

### 3. Nodo Function

Se agrega **prioridad** y **categoría** a cada correo.



Código utilizado:

```javascript
return items.map(item => {
  const email = item.json;
  let priority = "Baja";
  if (["Reunión urgente sobre el proyecto", "Aviso importante sobre tu cuenta bancaria", "Recordatorio de cita médica"].includes(email.subject)) {
    priority = "Alta";
  }

  let category = "General";
  if (["Reunión urgente sobre el proyecto", "Pago de nómina correspondiente a octubre", "Actualización del cronograma del proyecto Alfa"].includes(email.subject)) {
    category = "Trabajo";
  } else if (["Aviso importante sobre tu cuenta bancaria"].includes(email.subject)) {
    category = "Finanzas";
  } else if (["Recordatorio de cita médica"].includes(email.subject)) {
    category = "Salud";
  }

  return {
    json: { ...email, priority, category }
  };
});
```

---

### 4. Nodo IF

Separa los correos en **Prioridad Alta** y **Prioridad Baja**.



- Salida TRUE → Prioridad Alta
- Salida FALSE → Prioridad Baja

---

### 5. Nodo Debug

Muestra los resultados finales de los correos simulados con su **prioridad** y **categoría**.



Ejemplo de salida:

```json
[
  {
    "from": "gerente@empresa.com",
    "subject": "Reunión urgente sobre el proyecto",
    "body": "Necesitamos revisar los avances del proyecto hoy a las 5 pm.",
    "priority": "Alta",
    "category": "Trabajo"
  },
  {
    "from": "ventas@tiendaonline.com",
    "subject": "Promoción exclusiva: 50% de descuento",
    "body": "Aprovecha nuestras ofertas por tiempo limitado.",
    "priority": "Baja",
    "category": "Marketing"
  }
]
```

---

## Conclusión

Esta V1 permite **simular la clasificación automática de correos** usando **N8N** y conceptos de **MCP/LLM**, preparando el proyecto para la integración final con correos reales y acciones automatizadas.

---

## Instrucciones de Entrega

1. Subir este README.md a tu repositorio de GitHub.
2. Agregar capturas de los nodos en la carpeta `images/`.
3. Asegurarte de que el flujo en N8N se pueda ejecutar para demostrar la simulación.
