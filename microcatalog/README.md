# Microcatalog – Proyecto de Microservicios con Docker y Kubernetes  
**Versión v1 – Avance del Proyecto Final**

Este proyecto implementa una arquitectura basada en microservicios para gestionar autenticación de usuarios, productos y un frontend que consume los servicios mediante API. Cada microservicio está completamente aislado, contenerizado con Docker e implementado en un clúster de Kubernetes mediante Deployments, Services, ConfigMaps y Secrets.

---

# Arquitectura del Proyecto

El sistema está compuesto por **tres microservicios** independientes:

### **1. Auth Service (Python + FastAPI)**
Encargado del registro, login y validación de tokens JWT.  
Incluye:
- Hashing de contraseñas con bcrypt  
- Generación y validación de JWT  
- Endpoints protegidos  
- Uso de un Secret de Kubernetes para almacenar la clave privada

### **2. Products Service (Python + FastAPI)**
Proporciona operaciones CRUD para productos.  
Incluye:
- Validación de tokens contra el Auth Service  
- Configuración por medio de ConfigMaps  
- Comunicación REST entre microservicios

### **3. Frontend (Python + Tkinter / Web según la etapa)**
Interfaz gráfica que permite:
- Iniciar sesión  
- Listar productos  
- Crear, editar y eliminar productos  

El frontend se conecta a los Services de Kubernetes utilizando variables de entorno.

---

# 🐳 Contenerización con Docker

Cada microservicio está empaquetado e aislado mediante su propio Dockerfile, conteniendo:
- Código fuente  
- Dependencias  
- Configuraciones independientes  

Esto asegura que cada servicio funcione igual en cualquier entorno.

---

# ☸️ Orquestación con Kubernetes

El proyecto utiliza Kubernetes para administrar el ciclo de vida de los contenedores:

- **Deployments** → Crean y gestionan Pods de cada microservicio  
- **Services** → Permiten que los microservicios se comuniquen  
- **ConfigMaps** → Proveen ajustes como URLs internas  
- **Secrets** → Guardan información sensible como el SECRET_KEY  
- **NodePort** → Expone el frontend fuera del clúster  

Esto garantiza escalabilidad, resiliencia y actualizaciones sin downtime.

---

# 🔐 Seguridad

- JWT para autenticación  
- Hashing seguro  
- Comunicación entre microservicios mediante Services internos de Kubernetes  
- Secrets para evitar incluir claves en el código  

---

# 📦 Estructura del Proyecto

```
microcatalog/
 ├── auth_service/
 │    ├── main.py
 │    ├── requirements.txt
 │    └── Dockerfile
 ├── products_service/
 │    ├── main.py
 │    ├── requirements.txt
 │    └── Dockerfile
 ├── frontend/
 │    ├── main.py
 │    ├── requirements.txt
 │    └── Dockerfile
 ├── k8s/
 │    ├── auth-service.yaml
 │    ├── products-service.yaml
 │    ├── frontend.yaml
 │    ├── auth-secret.yaml
 │    ├── products-config.yaml
 │    └── frontend-config.yaml
 └── README.md
```

---

# 🚀 Tutorial Completo: Cómo Desplegar el Proyecto

Este tutorial permite que **cualquier persona**, sin saber nada de Kubernetes, pueda correr tu proyecto.

---

## 🔧 1. Instalar Herramientas Requeridas

### **Docker Desktop**
https://www.docker.com/products/docker-desktop/

Activa **Kubernetes** solo si lo piden, pero usaremos Minikube.

### **Kubectl**
https://kubernetes.io/docs/tasks/tools/

### **Minikube**
https://minikube.sigs.k8s.io/docs/start/

---

## 🚀 2. Iniciar Minikube

```bash
minikube start
```

Verifica que el clúster está activo:

```bash
kubectl get nodes
```

---

## 🏗️ 3. Construir las imágenes con Minikube

Primero conecta Docker al entorno de Minikube:

```bash
minikube docker-env
```

Luego ejecuta:

```bash
& minikube -p minikube docker-env | Invoke-Expression
```

Ahora construye las imágenes:

```bash
docker build -t auth_service:1.0 ./auth_service
docker build -t products_service:1.0 ./products_service
docker build -t frontend:1.0 ./frontend
```

---

## 🔐 4. Crear los Secrets y ConfigMaps

```bash
kubectl apply -f k8s/auth-secret.yaml
kubectl apply -f k8s/products-config.yaml
kubectl apply -f k8s/frontend-config.yaml
```

---

## ☸️ 5. Desplegar los microservicios

```bash
kubectl apply -f k8s/auth-service.yaml
kubectl apply -f k8s/products-service.yaml
kubectl apply -f k8s/frontend.yaml
```

Verifica:

```bash
kubectl get pods
kubectl get svc
```

---

## 🌐 6. Conectar al Frontend

El frontend usa NodePort, así que exponlo:

```bash
minikube service frontend
```

Esto abrirá automáticamente el navegador con una URL como:

```
http://192.168.49.2:30080
```

---

## ✔️ 7. Comprobar funcionamiento

- Inicia sesión  
- Agrega productos  
- Elimínalos  
- Revisa Pods en Kubernetes:

```bash
kubectl describe pod nombre-del-pod
```

---

# 📄 Estado del Proyecto (v1.1)

| Módulo | Estado | Detalles |
|-------|--------|----------|
| Auth Service | ✔️ Completo | Docker + K8s + Secret + JWT |
| Products Service | ✔️ Completo | CRUD + Validación JWT + ConfigMap |
| Frontend | ✔️ Funcional | Consume APIs del clúster |
| Docker | ✔️ Completo | Imágenes de los 3 servicios |
| Kubernetes | ✔️ Parcial | Falta Istio/monitorización y CI/CD |
| Seguridad | ✔️ Parcial | JWT + Secrets, falta TLS |
| Documentación | ✔️ Avanzada | README v1.1 listo |

---

# 📝 Próximos pasos (para la versión final)

- Agregar monitoreo (Opcional/Mínimo)  
- Preparar presentación final  
- Añadir pruebas simples  
- Agregar un pequeño pipeline CI/CD con GitHub Actions (si lo permites)  
- Opcional: Ingeniería del caos con `kubectl delete pod`  

---

# 🎉 Créditos

Proyecto desarrollado por **Paola Espinoza**, como implementación académica de arquitectura de microservicios con Docker y Kubernetes.

