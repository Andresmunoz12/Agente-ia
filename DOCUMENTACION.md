# 📞 AlphaTech AI Voice Assistant — Documentación del Proyecto

> **Última actualización:** Junio 2026  
> **Autor del proyecto:** Andrés Muñoz  
> **Repositorio:** `llamadas-agentes-ia`

---

## 1. DESCRIPCIÓN DEL PROYECTO

**AlphaTech AI Voice Assistant** es una aplicación web interactiva construida con **Python + Streamlit** que actúa como un **centro de atención al cliente impulsado por Inteligencia Artificial de voz**. El sistema permite a cualquier usuario iniciar una llamada de voz en tiempo real directamente desde el navegador y conversar con un agente virtual de IA entrenado para responder preguntas sobre pedidos, devoluciones, garantías y políticas de la empresa ficticia *AlphaTech*.

La aplicación integra la plataforma **Vapi.ai** como motor de voz conversacional, que se encarga de la síntesis de voz (TTS), reconocimiento de habla (STT) y el modelo de lenguaje (LLM) subyacente. La interfaz fue diseñada con estética **glassmorphism y dark mode premium**, haciendo uso de gradientes animados, micro-animaciones CSS y tipografía moderna.

### ¿Para qué sirve?
- **Demo comercial**: presentar a clientes o stakeholders cómo funciona un agente de IA de voz para atención al cliente.
- **Prototipo de call center virtual**: base para escalar hacia un sistema de atención real.
- **Plataforma de pruebas de voz**: permite cambiar la voz del asistente (acento, género, proveedor) sin tocar código.

### Stack tecnológico

| Componente           | Tecnología                              |
|----------------------|-----------------------------------------|
| Framework UI         | Streamlit 1.58                          |
| Base de datos        | SQLite (via módulo `sqlite3` nativo)    |
| Procesamiento datos  | Pandas 3.0                              |
| Motor de voz (IA)   | Vapi.ai (SDK JS + API REST)             |
| Proveedores de voz   | ElevenLabs, Cartesia                    |
| Contenedorización    | Docker + Docker Compose                 |
| Lenguaje             | Python 3.12                             |
| Estilos              | CSS custom (Glassmorphism + animaciones)|
| Tipografía           | Plus Jakarta Sans (Google Fonts)        |

---

## 2. ESTRUCTURA DEL PROYECTO

```
llamadas-agentes-ia/
│
├── app.py                    # Aplicación principal (UI + lógica de llamadas)
├── database.py               # Módulo de base de datos SQLite (CRUD de pedidos)
├── politicas.txt             # Documento de políticas de la empresa (referencia del agente)
├── alphatech_records.db      # Base de datos SQLite auto-generada
│
├── requirements.txt          # Dependencias Python (Streamlit, Pandas)
├── Dockerfile                # Imagen Docker de la aplicación
├── docker-compose.yml        # Orquestación del servicio
├── .env                      # Variables de entorno (API Keys)
├── .gitignore                # Archivos ignorados por Git
├── .dockerignore             # Archivos ignorados por Docker
└── explicacion.md            # Notas rápidas de arranque
```

---

## 3. FUNCIONALIDADES CLAVE

### 3.1 — Panel de Simulación de Llamada (Columna Izquierda)
- **Inicio de llamada de voz**: el usuario presiona "Iniciar Llamada de Voz" y el sistema solicita permiso de micrófono al navegador vía `getUserMedia`.
- **Estado en tiempo real**: el indicador `vapi-live-status` muestra el estado actual: *Verificando micrófono → Estableciendo WebRTC → Llamada Activa → El asistente habla → Escuchando tu voz*.
- **Animación del micrófono**: icono pulsante verde animado con `@keyframes pulse-green` cuando la llamada está activa; gris estático cuando está en espera.
- **Finalización de llamada**: el usuario puede cortar la llamada, lo que detiene el SDK de Vapi y reinicia el estado visual.

### 3.2 — Integración con Vapi.ai (JavaScript Bridge)
- El SDK de Vapi (`vapiSDK`) se inyecta dinámicamente en el `<head>` del documento padre mediante un iframe-bridge, ya que Streamlit renderiza componentes dentro de iframes.
- Se definen dos funciones globales en `window.parent`: `startVapiCall()` y `stopVapiCall()`.
- Se escuchan eventos del SDK: `call-start`, `call-end`, `speech-start`, `speech-end`, y `error`.
- El control del flujo de llamada (iniciar/detener) se activa reactivamente desde el estado de sesión de Streamlit (`st.session_state.llamando`).

### 3.3 — Configuración de Credenciales Vapi
- Sección colapsable que permite al usuario ingresar su **Public API Key** y **Assistant ID** de Vapi sin modificar el código fuente.
- Se usa la clave pública para iniciar llamadas en el navegador y la clave privada para actualizar la voz via API REST.

### 3.4 — Cambio Dinámico de Voz del Asistente
- El usuario puede seleccionar entre **5 voces preconfiguradas en español** (colombiano, español de España, femenino/masculino) de los proveedores ElevenLabs y Cartesia, o ingresar un ID de voz personalizado.
- Al presionar "Aplicar y Cambiar Voz", se hace un `PATCH` a la API de Vapi (`/assistant/{id}`) para actualizar la voz en caliente, sin necesidad de recrear el asistente.

### 3.5 — Base de Datos de Pedidos (Columna Derecha)
- Base de datos **SQLite local** con una tabla `pedidos` que contiene: ID del pedido, cliente, producto, estado y días desde entrega.
- Datos de demostración pre-cargados automáticamente al iniciar (4 pedidos: ALFA-101 a ALFA-104).
- Se visualizan en tiempo real en la interfaz mediante un **DataFrame interactivo de Pandas**.
- El agente de IA puede consultar estos datos para responder preguntas del usuario durante la llamada.

### 3.6 — Visualización de Políticas Empresariales
- El contenido de `politicas.txt` (políticas de devolución, envíos, garantías) se muestra en un área de texto de solo lectura.
- Este documento sirve como **contexto de referencia** para que el agente de voz responda con información correcta.

### 3.7 — Preguntas Sugeridas al Usuario
- Se muestran 4 tarjetas de ejemplo con frases que el usuario puede decir al agente: consultar un pedido, preguntar por devoluciones, tiempos de envío y garantías.

### 3.8 — Contenedorización Docker
- La aplicación se puede levantar con un solo comando `docker compose up --build`.
- Expone el puerto `8501` y se mantiene activa con `restart: unless-stopped`.

---

## 4. CÓMO EJECUTAR EL PROYECTO

### Opción A — Con Docker (Recomendado)
```bash
# Desde la raíz del proyecto
cd Documentos/llamadas-agentes-ia

docker compose up --build
```
Abrir en el navegador: **http://localhost:8501**

### Opción B — Entorno Local (Python)
```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

### Configuración inicial
1. Abrir la sección **"⚙️ CONFIGURACIÓN DE CREDENCIALES (VAPI)"** en la interfaz.
2. Ingresar tu **Vapi Public API Key** (obtenida en dashboard.vapi.ai → Account → API Keys).
3. Verificar el **Assistant ID** correcto.
4. (Opcional) Seleccionar y aplicar una voz diferente con la **Private API Key**.
5. Presionar **"🟩 Iniciar Llamada de Voz"** y conceder permisos de micrófono.

---

## 5. PASOS A SEGUIR PARA MEJORAR EL PROYECTO

A continuación se describen las mejoras priorizadas por impacto y complejidad, de menor a mayor esfuerzo:

---

### 🔴 ALTA PRIORIDAD — Seguridad y Estabilidad

#### 5.1 Mover las API Keys a variables de entorno seguras
**Problema actual:** Las claves de API de Vapi (`DEFAULT_PRIVATE_KEY`, `DEFAULT_ASSISTANT_ID`) están hardcodeadas directamente en `app.py`, lo cual es un riesgo de seguridad grave si el código es compartido o subido a un repositorio público.

**Solución:**
- Leer las claves desde el archivo `.env` usando la librería `python-dotenv`.
- Nunca exponer la **Private Key** en el frontend JavaScript.

```python
# requirements.txt → agregar: python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
DEFAULT_PRIVATE_KEY = os.getenv("VAPI_PRIVATE_KEY", "")
DEFAULT_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID", "")
```

```env
# .env
VAPI_PRIVATE_KEY=tu-clave-privada-aqui
VAPI_ASSISTANT_ID=tu-assistant-id-aqui
```

---

#### 5.2 Separar la Private Key del Public Key en la UI
**Problema actual:** Se usa la misma clave (`DEFAULT_PRIVATE_KEY`) para el campo de "Public API Key" (usado en el navegador) y para el campo de "Private API Key" (usado para actualizar la voz), lo que es una confusión y un error de seguridad.

**Solución:** Definir dos variables distintas: `VAPI_PUBLIC_KEY` y `VAPI_PRIVATE_KEY`, y usarlas correctamente en cada contexto.

---

### 🟠 MEDIA PRIORIDAD — Funcionalidad y Experiencia de Usuario

#### 5.3 Historial de Conversaciones
**Descripción:** Agregar un módulo que registre en la base de datos SQLite cada conversación iniciada: fecha, hora, duración aproximada y temas consultados.

**Beneficio:** Permite hacer seguimiento de las interacciones, identificar preguntas frecuentes y mejorar el entrenamiento del agente.

**Implementación sugerida:**
- Crear tabla `conversaciones` en `database.py`.
- Capturar eventos `call-start` y `call-end` del SDK de Vapi para registrar inicio/fin.
- Mostrar historial en una nueva pestaña de la interfaz.

---

#### 5.4 CRUD Completo de Pedidos en la UI
**Descripción:** Actualmente los pedidos son de solo lectura. Agregar formularios para **crear, editar y eliminar** pedidos directamente desde la interfaz, sin necesitar acceder a la base de datos manualmente.

**Implementación sugerida:**
- Formulario de Streamlit con campos: ID Pedido, Cliente, Producto, Estado, Días desde entrega.
- Botones de acción por cada fila del dataframe (Editar / Eliminar).
- Funciones adicionales en `database.py`: `insertar_pedido()`, `actualizar_pedido()`, `eliminar_pedido()`.

---

#### 5.5 Transcripción de la Llamada en Tiempo Real
**Descripción:** Mostrar en la interfaz el texto de lo que dice el usuario y el agente durante la llamada, aprovechando los eventos `transcript` del SDK de Vapi.

**Beneficio:** Mejora la accesibilidad y permite revisar lo conversado después de la llamada.

**Implementación sugerida:**
- Escuchar el evento `message` del SDK de Vapi para capturar transcripciones parciales y finales.
- Mostrar en un contenedor scrollable en la UI con colores diferenciados (usuario vs. agente).

---

#### 5.6 Panel de Métricas y Estadísticas
**Descripción:** Agregar un panel con KPIs básicos del sistema:
- Total de llamadas realizadas.
- Llamada más reciente.
- Pedido más consultado.
- Estado de conexión con la API de Vapi.

**Implementación sugerida:** Tarjetas de métricas en la parte superior de la interfaz usando `st.metric()`.

---

### 🟡 MEDIA-BAJA PRIORIDAD — Arquitectura y Escalabilidad

#### 5.7 Reemplazar SQLite por una base de datos en la nube
**Descripción:** SQLite funciona bien para demos locales, pero no es apropiado para múltiples usuarios simultáneos ni para entornos de producción. Migrar a **PostgreSQL** (con Docker) o usar un servicio como **Supabase** (PostgreSQL serverless gratuito).

**Beneficio:** Soporte multiusuario, persistencia real, consultas más robustas.

---

#### 5.8 Autenticación y Control de Acceso
**Descripción:** Agregar un sistema de login para que solo usuarios autorizados puedan acceder al panel de configuración y al historial de llamadas.

**Implementación sugerida:**
- Usar `streamlit-authenticator` para login básico con usuarios y contraseñas hasheadas.
- Separar roles: *Administrador* (acceso total) vs. *Demo* (solo puede iniciar llamadas).

---

#### 5.9 Multi-Asistente: Selección de Agente por Caso de Uso
**Descripción:** En lugar de un solo asistente de Vapi, permitir seleccionar entre múltiples agentes preconfigurados: ventas, soporte técnico, facturación, etc.

**Implementación sugerida:**
- Agregar un `st.selectbox` con los diferentes asistentes y sus IDs.
- Cada asistente tiene su propio prompt, voz y contexto de datos.

---

#### 5.10 Despliegue en Nube (Producción)
**Descripción:** Preparar la aplicación para ser desplegada en un servidor de producción accesible públicamente.

**Opciones recomendadas:**
- **Streamlit Community Cloud**: despliegue gratuito desde GitHub, ideal para demos.
- **Railway.app**: despliegue con Docker directo desde el repositorio.
- **DigitalOcean App Platform**: escalable con soporte nativo para contenedores.

**Pasos previos necesarios:**
1. Completar el paso 5.1 (variables de entorno).
2. Agregar un `volumes:` en `docker-compose.yml` para persistir la base de datos SQLite entre reinicios.
3. Configurar HTTPS (requerido por el navegador para acceder al micrófono).

---

### 🟢 BAJA PRIORIDAD — Calidad del Código

#### 5.11 Separar el JavaScript en archivos estáticos
**Descripción:** El código JavaScript del "Vapi Bridge" está embebido como string dentro de `app.py`, lo que dificulta su mantenimiento. Moverlo a archivos `.js` separados en una carpeta `/static`.

---

#### 5.12 Agregar pruebas unitarias
**Descripción:** Agregar tests para las funciones del módulo `database.py` (crear tablas, insertar, consultar) usando `pytest`.

---

#### 5.13 Logging y monitoreo de errores
**Descripción:** Implementar el módulo `logging` de Python para registrar errores, llamadas a la API de Vapi y eventos importantes en un archivo de log. Útil para debugging en producción.

---

## 6. RESUMEN DE PRIORIDADES

| # | Mejora                              | Impacto | Esfuerzo | Prioridad |
|---|-------------------------------------|---------|----------|-----------|
| 5.1 | Mover API Keys a `.env`          | Alto    | Bajo     | 🔴 Alta   |
| 5.2 | Separar Public/Private Key       | Alto    | Bajo     | 🔴 Alta   |
| 5.3 | Historial de conversaciones      | Alto    | Medio    | 🟠 Media  |
| 5.4 | CRUD completo de pedidos         | Medio   | Medio    | 🟠 Media  |
| 5.5 | Transcripción en tiempo real     | Alto    | Medio    | 🟠 Media  |
| 5.6 | Panel de métricas KPI            | Medio   | Bajo     | 🟠 Media  |
| 5.7 | Migrar a PostgreSQL              | Alto    | Alto     | 🟡 Media-Baja |
| 5.8 | Autenticación y roles            | Medio   | Medio    | 🟡 Media-Baja |
| 5.9 | Multi-asistente por caso de uso  | Medio   | Medio    | 🟡 Media-Baja |
| 5.10 | Despliegue en producción        | Alto    | Alto     | 🟡 Media-Baja |
| 5.11 | JS en archivos estáticos        | Bajo    | Bajo     | 🟢 Baja   |
| 5.12 | Pruebas unitarias               | Medio   | Medio    | 🟢 Baja   |
| 5.13 | Logging y monitoreo             | Medio   | Bajo     | 🟢 Baja   |

---

*Documentación generada automáticamente tras análisis del código fuente del proyecto.*
