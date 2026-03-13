import os
import yt_dlp

def descargar_musica(url, carpeta="Descargas"):
    """
    Descarga la música de YouTube sin usar cookies y emulando un cliente móvil.
    """
    try:
        # Limpiamos la URL por si acaso trae espacios
        url = url.strip()
        os.makedirs(carpeta, exist_ok=True)
        
        # Ruta de ffmpeg en Linux
        ffmpeg_path = '/usr/bin/ffmpeg'
        
        opciones = {
            # 'ba' busca el mejor audio. Si falla, 'best' busca lo mejor disponible (video+audio)
            'format': 'bestaudio/best',
            'outtmpl': f'{carpeta}/%(title)s.%(ext)s', 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '190',
            }],
            'ffmpeg_location': ffmpeg_path,
            
            'no_color': True,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'noplaylist': True,
            
            
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
                    'skip': ['dash', 'hls']
                }
            },
    
            'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
        }
        
        with yt_dlp.YoutubeDL(opciones) as ydl:
            print(f"Iniciando descarga (sin cookies) para: {url}")
            info = ydl.extract_info(url, download=True)
            
            if not info:
                raise Exception("YouTube no devolvió información del video.")
                
            archivo_descargado = ydl.prepare_filename(info)
            # El post-procesador de FFmpeg cambiará la extensión a .mp3
            archivo_final = os.path.splitext(archivo_descargado)[0] + ".mp3"
            
            return {
                'path': archivo_final,
                'title': info.get('title', 'Audio Desconocido'),
                'artist': info.get('uploader', 'Desconocido'),
                'duration': info.get('duration', 0)
            }
    except Exception as e:
        print(f"Error en la descarga (Modo Sin Cookies): {e}")
        raise e
