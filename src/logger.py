import datetime
import os

LOG_FILE = "descargas.log"

def registrar_descarga(user_id, user_name, song_title, url):
    """
    Guarda un registro de la descarga en un archivo de texto.
    """

    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    log_entry = f"[{ahora}] ID: {user_id} | Usuario: @{user_name} | Canción: {song_title} | URL: {url}\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"📝 Log guardado: {song_title}")
    except Exception as e:
        print(f"Error al escribir en el log: {e}")
