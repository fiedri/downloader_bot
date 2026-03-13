import telebot
import os
from src.music import descargar_musica
from src.logger import registrar_descarga
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
telebot.apihelper.CONNECT_TIMEOUT = 60
telebot.apihelper.READ_TIMEOUT = 60

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
👋 <b>¡Hola! Soy YtdownMusic</b>

Soy tu asistente personal para descargar música de YouTube. 🎧
Simplemente envíame el enlace de cualquier video o canción de YouTube y yo me encargaré de extraer el audio en la mejor calidad.

Escribe /help para más información.\
""")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """\
📖 <b>¿Cómo usar el bot?</b>

1. Ve a YouTube y copia el enlace del video o canción que deseas.
2. Pega el enlace aquí en el chat y envíamelo.
3. Espera unos momentos mientras proceso y descargo el audio.
4. ¡Disfruta tu música directamente en Telegram! 🎶
""")

@bot.message_handler(content_types=['text'])
def download(message):
    try:
        urlyt = ("https://youtu.be", "https://www.youtube.com", "https://youtube.com", "https://music.youtube.com")
        if message.text.strip().startswith(urlyt):
            msg = bot.reply_to(message, "🔍 <i>Buscando y procesando enlace...</i>")
            
            try:
                bot.edit_message_text("⬇️ <i>Descargando audio en alta calidad...</i>", chat_id=message.chat.id, message_id=msg.message_id)
                audio_info = descargar_musica(message.text)
              
                bot.edit_message_text("⬆️ <i>Subiendo canción a Telegram...</i>", chat_id=message.chat.id, message_id=msg.message_id)
                
                with open(audio_info['path'], 'rb') as cancion:
                    bot.send_chat_action(message.chat.id, 'upload_audio')
                    bot.send_audio(
                        chat_id=message.chat.id, 
                        audio=cancion,
                        title=audio_info['title'],
                        performer=audio_info['artist'],
                        duration=audio_info['duration']
                    )
                
                registrar_descarga(
                    message.from_user.id, 
                    message.from_user.username or message.from_user.first_name, 
                    audio_info['title'], 
                    message.text
                )

                bot.delete_message(message.chat.id, msg.message_id)
                if os.path.exists(audio_info['path']):
                    os.remove(audio_info['path'])
                
            except Exception as e:
                bot.edit_message_text(f"❌ <b>Error al procesar la descarga:</b>\n<code>{str(e)}</code>", chat_id=message.chat.id, message_id=msg.message_id)
        else:
            bot.reply_to(message, "⚠️ <b>Enlace no válido.</b>\nPor favor, envíame un enlace correcto de YouTube.")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Ocurrió un error inesperado:</b>\n<code>{str(e)}</code>")

if __name__ == '__main__':
    print("Iniciando bot...")
    bot.infinity_polling()
