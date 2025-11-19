# 🗳️ Sistema de Votación Electrónica Seguro (Criptografía)

Este proyecto es una plataforma web desarrollada en **Django** que implementa un sistema de votación seguro. Utiliza estándares criptográficos avanzados (**RSA y AES**) para garantizar la **confidencialidad, integridad y no repudio** de cada voto emitido.

---

## 🚀 Características del Sistema

### 1. **Infraestructura de Llave Pública (PKI)**

* Cada votante genera un par de llaves **RSA de 2048 bits**.
* La **llave pública** se almacena en el servidor.
* La **llave privada** se descarga al dispositivo del usuario (archivo `.key`).

### 2. **Seguridad del Voto**

* **Firma Digital:**
  Se genera un hash SHA-256 del voto y se firma con la llave privada del usuario.
* **Cifrado Híbrido:**
  El voto se cifra con **AES-256 CBC**, garantizando confidencialidad.

### 3. **Transparencia**

* Panel de resultados con gráficos en tiempo real.
* Módulo de auditoría para administradores (visualización de firmas y hashes).
* Validación de estado de llaves para los votantes.

---

## 🛠️ Stack Tecnológico

| Componente        | Tecnología / Librería | Versión | Descripción                                 |
| ----------------- | --------------------- | ------- | ------------------------------------------- |
| **Backend**       | Django                | 5.2.8   | Framework web principal.                    |
| **Criptografía**  | PyCryptodome          | 3.23.0  | RSA, AES y SHA256.                          |
| **Configuración** | Python-Decouple       | 3.8     | Gestión de variables de entorno.            |
| **Base de Datos** | DJ-Database-URL       | 3.0.1   | Conexión agnóstica (SQLite / PostgreSQL).   |
| **Estáticos**     | WhiteNoise            | 6.11.0  | Manejo de archivos estáticos en producción. |
| **Servidor**      | Gunicorn              | 23.0.0  | Servidor WSGI para despliegue.              |

---

## ⚙️ Instalación en Local

> Requisitos: **Python 3.10+**, **Git**

### **1. Clonar el Repositorio**

```bash
git clone https://github.com/LilianaVo/Sistema-Votacion-Seguro-CryptoVoting.git
cd Sistema-Votacion-Seguro-CryptoVoting
```

---

### **2. Configurar Entorno Virtual**

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

---

### **3. Instalar Dependencias**

```bash
pip install -r requirements.txt
```

---

### **4. Crear Archivo .env**

Dentro del directorio raíz (donde está `manage.py`):

```ini
DEBUG=True
SECRET_KEY=pon_aqui_una_clave_segura_y_larga
# DATABASE_URL se puede omitir en local (usa SQLite por defecto)
```

---

### **5. Inicializar Base de Datos**

```bash
python manage.py migrate
```

---

### **6. Crear Usuario Administrador**

```bash
python manage.py createsuperuser
```

---

### **7. Ejecutar el Servidor**

```bash
python manage.py runserver
```

El sistema estará disponible en:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

# ☁️ Despliegue en Producción (Render)

### **Build Command**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### **Start Command**

```bash
gunicorn voting_project.wsgi:application
```

---

# 🔄 Mantenimiento: Reinicio Rápido del Sistema

> **Advertencia:** haz un respaldo de la base de datos antes de ejecutar estos comandos si quieres conservar datos reales. Estos pasos **eliminan usuarios y votos** (excepto el superusuario).

---

### 1. Abrir la consola de Django (en la terminal de VS Code)

```bash
python manage.py shell
```

---

### 2. Ejecutar los comandos de limpieza (pega uno por uno)

**A) Importar modelos**

```python
from django.contrib.auth.models import User
from voting.models import Vote, VoterProfile
```

**B) Eliminar todos los usuarios que no sean superusuario**

```python
User.objects.filter(is_superuser=False).delete()
```

**C) Borrar todos los votos y reiniciar el estado de voto de los perfiles**

```python
Vote.objects.all().delete()
VoterProfile.objects.update(has_voted=False)
```

---

### 3. Salir de la consola

```python
exit()
```

---

# 👥 Desarrollado por

* **Roja Mares Luis Iván**
* **Lee Obando Ileana Verónica**

**Materia:** Criptografía
**Profesor:** Dr. Alfonso Francisco De Abiega L Eglisse
**Grupo:** 02
**Facultad de Ingeniería - UNAM**

