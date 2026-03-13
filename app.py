import telebot
import os
from telebot import types
from src.downloader import descargar_contenido
from src.logger import registrar_descarga
from dotenv import load_dotenv
import uuid

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
telebot.apihelper.CONNECT_TIMEOUT = 60
telebot.apihelper.READ_TIMEOUT = 60

# Diccionario para almacenar URLs temporalmente con claves únicas
pending_downloads = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
👋 <b>¡Hola! Soy tu Asistente de Descarga</b> 🚀

Puedo descargar contenido de muchas redes sociales:
📺 YouTube
🤳 TikTok / Instagram
🐦 Twitter (X)
☁️ SoundCloud... ¡y más!

<b>¡Simplemente envíame el enlace!</b>\
<i>Desarrollado por @fiedri</i>
""")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """\
📖 <b>¿Cómo usar el bot?</b>

1. Pega el enlace aquí en el chat y envíamelo.
2. Espera unos momentos mientras proceso la descarga.

<b>Fuentes comprobadas</b>
- youtube
- Tiktok (sin marca de agua)
- Instagram (sin marca de agua)
- x
                 
<b>Limitantes</b>
- Contenido que supere los 50 mb
""")

@bot.message_handler(content_types=['text'])
def ask_format(message):
    # Detectar si el texto contiene un enlace (simplificado)
    if "http://" in message.text or "https://" in message.text:
        # Generar una clave única para la URL
        key = str(uuid.uuid4())
        pending_downloads[key] = message.text
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_audio = types.InlineKeyboardButton("🎵 Audio (MP3)", callback_data=f"audio,{key}")
        btn_video = types.InlineKeyboardButton("🎬 Video (MP4)", callback_data=f"video,{key}")
        markup.add(btn_audio, btn_video)
        
        bot.reply_to(message, "🎶 <b>¿Qué formato deseas descargar?</b>", reply_markup=markup)
    else:
        bot.reply_to(message, "⚠️ Por favor, envíame un enlace válido.")

@bot.callback_query_handler(func=lambda call: True)
def process_download(call):
    data = call.data.split(',')
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    if len(data) != 2:
        bot.answer_callback_query(call.id, "Datos inválidos.")
        return
    
    tipo, key = data
    url = pending_downloads.pop(key, None)
    if not url:
        bot.answer_callback_query(call.id, "Enlace expirado o inválido.")
        return
    
    bot.edit_message_text(f"⏳ <b>Procesando tu {tipo}...</b>", chat_id, msg_id)
    try:
        info = descargar_contenido(url, tipo)
    except Exception as e:
        bot.edit_message_text(f"❌ <b>Error al descargar:</b> {str(e)}", chat_id, msg_id)
        return
    
    if not os.path.exists(info['path']):
        bot.edit_message_text("❌ <b>Error: Archivo no encontrado después de la descarga.</b>", chat_id, msg_id)
        return
    
    bot.edit_message_text(f"⬆️ <b>Subiendo {tipo} a Telegram...</b>", chat_id, msg_id)
    registrar_descarga(chat_id, call.message.from_user.username or call.message.from_user.first_name, info['title'], url)
    with open(info['path'], 'rb') as file:
        bot.send_chat_action(chat_id, 'upload_video' if tipo == 'video' else 'upload_audio')
            
        if tipo == 'audio':
            bot.send_audio(
                chat_id, 
                file, 
                title=info['title'], 
                performer=info['artist'], 
                duration=info['duration']
                )
        else:
            print("enviando ")
            bot.send_video(
                chat_id, 
                file, 
                caption=f"🎥 <b>{info['title']}</b>"
            )

        bot.delete_message(chat_id, msg_id)
        if os.path.exists(info['path']):
            os.remove(info['path'])
if __name__ == '__main__':
    print("Iniciando bot...")
    bot.infinity_polling()
