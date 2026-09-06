# Ejecutar el proyecto - llamadas-agentes-ia

Este documento describe pasos para ejecutar el proyecto localmente y con Docker.

Requisitos
- Python 3.8+ (recomendado 3.10/3.11)
- `pip` y opcionalmente `virtualenv`
- Si usas Docker: `docker` y `docker-compose` / `docker compose`

1) Clonar / situarse en el proyecto
```bash
cd /ruta/al/proyecto/llamadas-agentes-ia
pwd
```

2) Configurar entorno (.env)
- Verifica que exista el archivo `.env` en la raíz del proyecto y que contenga `VAPI_PUBLIC_KEY`.
- Si no existe, crea uno y añade la clave pública (o privadas si las tienes):
```bash
# crear .env con la clave pública
cat > .env <<EOF
VAPI_PUBLIC_KEY=tu-clave-publica-aqui
# VAPI_PRIVATE_KEY=tu-clave-privada-aqui
# VAPI_ASSISTANT_ID=tu-assistant-id-aqui
EOF
```

3) Instalación local (recomendado)
```bash
# crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate

# instalar dependencias
pip install -r requirements.txt
```

4) Ejecutar la aplicación
```bash
streamlit run app.py
```
- Abre en tu navegador: http://localhost:8501
- En la sección `⚙️ CONFIGURACIÓN DE CREDENCIALES (VAPI)` puedes ver/modificar la clave pública y el `assistant id` desde la UI.

5) Ejecutar con Docker (opcional)
- Si prefieres usar Docker y hay `Dockerfile`/`docker-compose.yml`, levanta el servicio:
```bash
# construir y levantar
docker compose up --build
# o, si usas la versión antigua:
# docker-compose up --build
```
- Revisa los logs en la terminal y accede en http://localhost:8501

6) Notas y resolución de problemas
- Error 401: revisa que `VAPI_PUBLIC_KEY` esté definida correctamente en `.env` y que la UI muestre la misma clave.
- Si cambias `.env` mientras la app está en ejecución, reinicia Streamlit para recargar variables.
- No subas el archivo `.env` a repositorios públicos. Añade `.env` a `.gitignore` si aún no está.

7) Limpieza rápida
```bash
# desactivar entorno virtual
deactivate
# detener docker
docker compose down
```

Si quieres, puedo también añadir una entrada a `.gitignore` para ignorar `.env` y commitear los cambios.