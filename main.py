import mysql.connector
from telegram.ext import Updater, MessageHandler, Filters

# Konfigurasi database
db_config = {
    'host': '188.166.231.207',
    'user': 'diskon',
    'password': 'aaaaaaac',
    'database': 'diskon'
}

# Inisialisasi koneksi database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Fungsi untuk menyimpan postingan ke database
def save_to_database(update, context):
    message = update.message
    image_link = None
    caption = None

    # Mendapatkan link gambar (jika ada)
    if message.photo:
        image_link = message.photo[-1].file_id

    # Mendapatkan caption teks
    if message.caption:
        caption = message.caption

    # Menyimpan ke database
    insert_query = "INSERT INTO posts (image_link, caption) VALUES (%s, %s)"
    cursor.execute(insert_query, (image_link, caption))
    conn.commit()

# Fungsi utama
def main():
    # Token bot Telegram, ganti dengan token bot Anda
    telegram_token = '5916688383:AAEQmWAhErzCidtIrIIk41VxFgbW0_FnetY'

    # Inisialisasi updater
    updater = Updater(token=telegram_token, use_context=True)
    dp = updater.dispatcher

    # Menambahkan handler untuk pesan dari channel dengan gambar dan caption
    dp.add_handler(MessageHandler(Filters.chat(chat_id='@racuntest') & Filters.photo & Filters.caption, save_to_database))

    # Memulai polling
    updater.start_polling()
    updater.idle()

    # Tutup koneksi database setelah bot dimatikan
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
