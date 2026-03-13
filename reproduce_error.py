import os
import yt_dlp
from src.downloader import descargar_contenido

# URL de prueba (un video corto de YouTube)
url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" 

try:
    print("Probando descarga de video...")
    resultado = descargar_contenido(url, tipo='video')
    print("Resultado:", resultado)
except Exception as e:
    import traceback
    traceback.print_exc()
