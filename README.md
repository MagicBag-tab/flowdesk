# FlowDesk - Infraestructura como Código con Docker

Este proyecto implementa un entorno completo de desarrollo utilizando el enfoque de Infraestructura como Código (IaC) mediante Docker. El sistema integra backend, frontend y base de datos en una arquitectura modular, permitiendo su despliegue automatizado y replicable.

---

## 1. Arquitectura del Proyecto

El proyecto sigue una estructura **monorepo modular**, donde cada componente se encuentra desacoplado en su propio directorio:

```
project-root/
│
├── backend-python/     # API REST desarrollada con FastAPI
├── frontend/           # Aplicación web desarrollada con Vue
├── database/           # Scripts de inicialización de base de datos en postgres
│
├── docker-compose.yml  # Definición y orquestación de servicios
├── .env                # Variables de entorno
└── README.md
```

---

## 2. Tecnologías Utilizadas

* Backend: Python (FastAPI)
* Frontend: Vue.js (Vite + Nginx)
* Base de datos: PostgreSQL
* Contenerización: Docker
* Orquestación: Docker Compose

---

## 3. Servicios Definidos

El entorno está compuesto por los siguientes servicios:

| Servicio       | Descripción                         |
| -------------- | ----------------------------------- |
| backend-python | API principal del sistema           |
| frontend       | Interfaz de usuario                 |
| database       | Sistema de gestión de base de datos |

---

## 4. Puertos Utilizados

| Servicio   | Puerto local | Puerto contenedor |
| ---------- | ------------ | ----------------- |
| Backend    | 8080         | 8000              |
| Frontend   | 3000         | 80                |
| PostgreSQL | 5432         | 5432              |

---

## 5. Variables de Entorno

El archivo `.env` contiene la configuración del sistema:

```
DB_HOST=database
DB_PORT=5432
DB_NAME=flowdeskdb
DB_USER=postgres
DB_PASSWORD=postgres
APP_PORT=8080
```

---

## 6. Ejecución del Proyecto

### 6.1 Clonar el repositorio

```
git clone <repo-url>
cd project-root
```

### 6.2 Construir y levantar los servicios

```
docker-compose up --build
```

Este comando construye las imágenes necesarias y levanta todos los servicios definidos.

---

## 7. Acceso a los Servicios

Una vez iniciado el entorno, se puede acceder a:

* Backend: http://localhost:8080
* Frontend: http://localhost:3000
* Base de datos: localhost:5432

---

## 8. Inicialización de Base de Datos

La base de datos se inicializa automáticamente mediante el script:

```
database/init.sql
```

Este archivo contiene la definición de tablas y estructura del sistema, y se ejecuta automáticamente al crear el contenedor por primera vez.

---

## 9. Persistencia de Datos

Se utiliza un volumen de Docker para garantizar la persistencia:

```
postgres_data
```

Esto permite conservar la información incluso después de detener o eliminar los contenedores.

---

## 10. Conceptos Implementados

* Infraestructura como Código (IaC)
* Contenerización de aplicaciones
* Orquestación de múltiples servicios
* Separación de responsabilidades
* Automatización del entorno de desarrollo
* Persistencia de datos mediante volúmenes

---

## 11. Escalabilidad

El proyecto está diseñado para permitir:
* Extensión de servicios adicionales
* Adaptación a entornos de producción

---

## 12. Evidencia

El proyecto incluye evidencia de funcionamiento mediante un video que demuestra:

* Construcción del entorno
* Ejecución de servicios
* Funcionamiento del backend
* Funcionamiento del frontend
* Conexión a la base de datos

---

## 13. Información Académica

Proyecto desarrollado para el curso de Ingeniería de Software.
Universidad del Valle de Guatemala.
