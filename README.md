# NeoDownloader bot
El bot permite la descarga de audio y video de las plataformas más influyentes del mercado actual, optimizando la entrega para cumplir con las restricciones de la API de Telegram.
## Capacidades
 * Multi-Plataforma: Soporte para YouTube, X (Twitter), Instagram y TikTok (sin marcas de agua).
 * Formatos Flexibles: Selección inteligente entre MP3 (Audio) y MP4 (Video).
 * Optimización de Carga: Sistema de control de peso automático limitado a 50MB para garantizar la compatibilidad con los servidores de Telegram.
 * Limpieza de Servidor: Gestión de archivos temporales integrada para mantener el almacenamiento optimizado.
## Instalación
 * Entorno: Asegúrate de tener Python 3.10+ y FFmpeg instalado en el sistema (el motor de procesamiento).
 * Dependencias:
   `pip install -r requirements.txt`

 * Configuración: Crea un archivo .env en la raíz del proyecto:
   `BOT_TOKEN=TU_TELEGRAM_TOKEN_AQUI`

 * Ejecución:
   `python app.py`

## Uso
Simplemente envía un enlace de cualquier red social soportada. El bot desplegará un menú interactivo para que elijas el formato.
Ejemplo de flujo:
Link de TikTok -> Elección: Video sin marca de agua -> Procesamiento -> Envío de MP4 (<50MB).
