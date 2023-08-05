import telebot
import requests

# Ganti 'TOKEN_BOT_ANDA' dengan token bot Telegram Anda
TOKEN = '6536507456:AAHbnpHE4YHAb7_fZ7427C4ayHDoA600j4o'
bot = telebot.TeleBot(TOKEN)

# Ganti 'TOKEN_REMOVEBG_API' dengan token API Remove.bg Anda
REMOVEBG_API_KEY = 'eTUAarhkKeRUwpJJm9ZJYYw4'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! selamat datang di bot remove background by @azigaming404 Kirimkan gambarnya bro untuk menghapus backgroundnya.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        # Kirim permintaan ke Remove.bg API untuk menghapus background gambar
        response = requests.post('https://api.remove.bg/v1.0/removebg', data={'image_url': file_url}, headers={'X-Api-Key': REMOVEBG_API_KEY})

        if response.status_code == 200:
            # Simpan gambar hasil dan kirimkan ke pengguna
            with open('removed_bg.png', 'wb') as f:
                f.write(response.content)
            bot.send_document(message.chat.id, open('removed_bg.png', 'rb'))
        else:
            bot.reply_to(message, "Maaf, tidak dapat menghapus background gambar.")

    except Exception as e:
        bot.reply_to(message, "Terjadi kesalahan saat memproses gambar.")

bot.polling()
