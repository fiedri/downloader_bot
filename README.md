# Bot de Telegram

Este es un bot de Telegram que permite descargar música de YouTube en formato MP3. Simplemente envía el enlace de un video de YouTube y el bot descargará la canción y te la enviará.

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Asegúrate de tener Python instalado en tu sistema.
3. Instala las dependencias necesarias ejecutando el siguiente comando en la terminal:

   ```bash
   pip install -r requirements.txt

4. Configura el archivo .env con tu token de bot de Telegram. Ejemplo:
TOKENBOT=YOUR_TELEGRAM_TOKEN

5. Ejecuta el bot con el siguiente comando:

## Uso
Envía un enlace de YouTube al bot. Por ejemplo:

1. Envía el siguiente enlace al bot:
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

2. El bot procesará el enlace y te responderá con un archivo MP3 descargado



1. Nivel Principiante: El Logger (logger.py)
  Concepto: Manejo de archivos y fechas.
   * Qué aprenderás: Cómo abrir archivos en modo "añadir" (a), cómo
     formatear fechas con datetime y cómo usar f-strings para crear
     mensajes limpios.
   * Reto para ti: Intenta añadir al comentario: ¿Qué pasaría si el
     archivo no existe? (Pista: Python lo crea solo si usas el modo
     a).


  2. Nivel Intermedio: El Motor de Descarga (downloader.py)
  Concepto: Diccionarios de configuración y librerías externas.
   * Qué aprenderás:
       * Diccionarios: Casi todas las opciones de yt-dlp se pasan
         como un diccionario ({ 'key': 'value' }).
       * Lógica de decisión: Cómo usar un if/else para cambiar el
         comportamiento del programa dependiendo de si el usuario
         quiere audio o video.
       * FFmpeg: Entenderás que este script es solo un "puente" que
         le da órdenes a un programa de terminal llamado FFmpeg.
   * Idea para aprender: Busca en Google qué significa cada opción
  3. Nivel Avanzado: El Cerebro del Bot (app.py)
  Concepto: Programación orientada a eventos y decoradores.
   * Qué aprenderás:
       * Decoradores (@bot.message_handler): Es una forma de
         decirle a Python: "Cuando pase X cosa en Telegram, ejecuta
         esta función".
       * Botones Inline: Cómo crear interfaces interactivas que no
         dependen solo de texto.
       * Callbacks: Es la parte más difícil. Cuando pulsas un
         botón, Telegram no envía un "mensaje", envía un
         "callback". Tienes que aprender a separar los datos (el
         callback_data).
       * Gestión de archivos temporales: Por qué es vital usar
         os.remove() para no llenar el servidor de basura.
