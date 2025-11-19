# 🗳️ Sistema de Votación Electrónica Seguro (Criptografía)

Este proyecto es una plataforma web desarrollada en **Django** que implementa un sistema de votación seguro. Utiliza estándares criptográficos avanzados (RSA y AES) para garantizar la **confidencialidad, integridad y no repudio** de cada voto emitido.

## 🚀 Características del Sistema

1.  **Infraestructura de Llave Pública (PKI):**
    * Cada votante genera un par de llaves **RSA de 2048 bits**.
    * La llave pública se almacena en el servidor.
    * La llave privada se descarga al dispositivo del usuario (archivo `.key`).

2.  **Seguridad del Voto:**
    * **Firma Digital:** Se crea un hash (SHA-256) del voto y se firma con la llave privada del usuario para garantizar autenticidad.
    * **Cifrado Híbrido:** El contenido del voto se cifra utilizando **AES-256** (modo CBC) para asegurar que solo el sistema pueda procesarlo (Confidencialidad).

3.  **Transparencia:**
    * Tablero de resultados con gráficos en tiempo real.
    * Módulo de auditoría para administradores (visualización de firmas y hashes).
    * Validación de estado de llaves para los usuarios.

## 🛠️ Stack Tecnológico

El proyecto fue construido utilizando las siguientes tecnologías y librerías:

| Componente | Tecnología / Librería | Versión | Descripción |
| :--- | :--- | :--- | :--- |
| **Backend** | **Django** | 5.2.8 | Framework web principal. |
| **Criptografía** | **PyCryptodome** | 3.23.0 | Implementación de algoritmos RSA, AES y SHA256. |
| **Configuración** | **Python-Decouple** | 3.8 | Gestión segura de variables de entorno (.env). |
| **Base de Datos** | **DJ-Database-URL** | 3.0.1 | Conexión agnóstica a BD (PostgreSQL en producción). |
| **Estáticos** | **WhiteNoise** | 6.11.0 | Servicio de archivos CSS/JS en producción. |
| **Servidor** | **Gunicorn** | 23.0.0 | Servidor HTTP WSGI para el despliegue. |

## ⚙️ Instrucciones de Instalación (Local)

Requisitos previos: Tener instalado **Python 3.10** o superior y **Git**.

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/LilianaVo/Sistema-Votacion-Seguro-CryptoVoting.git](https://github.com/LilianaVo/Sistema-Votacion-Seguro-CryptoVoting.git)
cd Sistema-Votacion-Seguro-CryptoVoting
