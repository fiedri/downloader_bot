import os
import yt_dlp

def descargar_contenido(url, tipo='audio', carpeta="Descargas"):
    """
    Descarga contenido con límites estrictos y limpieza automática de errores.
    """
    archivo_temporal = None
    info = None
    razon_filtrado = None
    
    try:
        url = url.strip()
        os.makedirs(carpeta, exist_ok=True)
        
        LIMITE_MB = 50
        LIMITE_BYTES = LIMITE_MB * 1024 * 1024

        def filtro_inteligente(info_dict, *, incomplete):
            nonlocal razon_filtrado
            duracion = info_dict.get('duration')
            
            if tipo == 'audio':
                
                if duracion and (23750 * duracion) > LIMITE_BYTES:
                    razon_filtrado = "LIMITE_ERROR"
                    return f"Audio demasiado largo (~{duracion/60:.1f}MB)"
                return None
            
            
            peso = info_dict.get('filesize') or info_dict.get('filesize_approx')
            if peso and peso > LIMITE_BYTES:
                razon_filtrado = "LIMITE_ERROR"
                return f"El video ({peso/1e6:.1f}MB) excede el límite"
            
            return None


        def hook_seguridad(d):
            nonlocal archivo_temporal
            archivo_temporal = d.get('filename')
            if d["status"] == "downloading":
                descargado = d.get('downloaded_bytes', 0)
                if descargado > LIMITE_BYTES:
                    raise Exception("LIMITE_ALCANZADO")

        ffmpeg_path = '/usr/bin/ffmpeg'
        
        opciones = {
            'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg_path,
            'progress_hooks': [hook_seguridad],
            'match_filter': filtro_inteligente,
            'restrictfilenames': True,
            'windowsfilenames': True,
            'no_color': True,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'noplaylist': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'ios'], 'skip': ['dash', 'hls']}},
            'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
        }

        if tipo == 'audio':
            opciones.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '190'}],
            })
        
        with yt_dlp.YoutubeDL(opciones) as ydl:
            
            info = ydl.extract_info(url, download=False)
            if not info or razon_filtrado == "LIMITE_ERROR":
                raise Exception("LIMITE_ERROR")
            
            
            if tipo == 'video':
                dur = info.get('duration', 0)
                ydl.params['format'] = 'bestvideo[height<=720]+bestaudio/best' if dur <= 60 else 'bestvideo[height<=480]+bestaudio/best'
            
            
            print(f"Iniciando descarga ({tipo})...")
            info_final = ydl.process_ie_result(info, download=True)
            
            
            if not info_final or 'requested_downloads' not in info_final:
                raise Exception("LIMITE_ERROR")
            
            
            archivo_final = info_final['requested_downloads'][0]['filepath']
            if tipo == 'audio' and not archivo_final.lower().endswith('.mp3'):
                archivo_final = os.path.splitext(archivo_final)[0] + ".mp3"
            
            if not os.path.exists(archivo_final):
                raise FileNotFoundError(f"No se pudo localizar el archivo final en: {archivo_final}")
            
            return {
                'path': archivo_final,
                'size_mb': round(os.path.getsize(archivo_final) / (1024 * 1024), 2),
                'title': info.get('title', 'Desconocido'),
                'artist': info.get('uploader', 'Desconocido'),
                'duration': info.get('duration', 0)
            }

    except Exception as e:
        error_msg = str(e)
        if "LIMITE_ALCANZADO" in error_msg or "LIMITE_ERROR" in error_msg:
            posibles_basuras = []
            if archivo_temporal:
                posibles_basuras.extend([archivo_temporal, archivo_temporal + ".part", archivo_temporal + ".ytdl"])
            if info:
                try:
                    with yt_dlp.YoutubeDL(opciones) as ydl_clean:
                        nombre_teorico = ydl_clean.prepare_filename(info)
                        posibles_basuras.extend([nombre_teorico, nombre_teorico + ".part", nombre_teorico + ".ytdl", os.path.splitext(nombre_teorico)[0] + ".mp3"])
                except: pass
            for ruta in set(posibles_basuras):
                if ruta and os.path.exists(ruta):
                    try: os.remove(ruta)
                    except: pass
            
            msg_usuario = f"Descarga cancelada: El archivo excede el límite de {LIMITE_MB}MB permitidos."
            print(f"Error: {msg_usuario}")
            raise Exception(msg_usuario)
            
        print(f"Error en la descarga: {e}")
        raise e
