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

Para una persona que **quiere usar tu proyecto desde VS Code**, estos son **los pasos exactos y mínimos** que debe hacer **antes de poder ejecutarlo**. Esto lo puedes poner también en tu README si quieres.

---

# ✅ ¿Qué necesita descargar/instalar primero?

## 1️⃣ **Instalar VS Code**

Descargar desde la página oficial:
[https://code.visualstudio.com/](https://code.visualstudio.com/)

---

## 2️⃣ **Instalar Python 3.10 o superior**

El proyecto usa Python, así que es indispensable instalarlo:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

> Asegúrate de marcar **“Add Python to PATH”** durante la instalación (muy importante).

---

## 3️⃣ **Instalar Git**

Es necesario para descargar el repositorio desde GitHub.
[https://git-scm.com/downloads](https://git-scm.com/downloads)

---

## 4️⃣ **Clonar el proyecto dentro de VS Code**

En VS Code:

**View → Command Palette → Git: Clone**

Pegar tu repo:

```
https://github.com/LilianaVo/Sistema-Votacion-Seguro-CryptoVoting.git
```

O con terminal integrada:

```bash
git clone https://github.com/LilianaVo/Sistema-Votacion-Seguro-CryptoVoting.git
cd Sistema-Votacion-Seguro-CryptoVoting
```

---

## 5️⃣ **Crear un entorno virtual (venv)**

Necesario para instalar las librerías sin afectar el sistema.

```bash
python -m venv venv
```

Activar:

### Windows:

```bash
.\venv\Scripts\activate
```

### Mac / Linux:

```bash
source venv/bin/activate
```

---

## 6️⃣ **Instalar las dependencias**

Estas vienen en `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 7️⃣ **Crear archivo `.env`**

En el mismo nivel que `manage.py` crear:

```ini
DEBUG=True
SECRET_KEY=escribe_una_clave_segura
```

---

## 8️⃣ **Inicializar la base de datos**

```bash
python manage.py migrate
```

---

## 9️⃣ **Crear un superusuario (admin)**

```bash
python manage.py createsuperuser
```

---

## 🔟 Ejecutar el servidor

```bash
python manage.py runserver
```

Acceder en:
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

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

* **Materia:** Criptografía
* **Profesor:** Dr. Alfonso Francisco De Abiega L Eglisse
* **Grupo:** 02
* **Facultad de Ingeniería - UNAM**

