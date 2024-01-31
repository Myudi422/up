from pyrogram import Client, filters
from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Konfigurasi database
engine = create_engine('mysql+mysqlconnector://diskon:aaaaaaac@188.166.231.207:3306/diskon', echo=True)
Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    image_link = Column(String)
    caption = Column(Text)

# Inisialisasi database
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

# Inisialisasi bot Pyrogram
api_id = '7120601'
api_hash = 'aebd45c2c14b36c2c91dec3cf5e8ee9a'
bot_token = '5916688383:AAEQmWAhErzCidtIrIIk41VxFgbW0_FnetY'

channel_username = 'racuntest'  # Ganti dengan username channel Anda

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Fungsi untuk menyimpan postingan ke database
def save_to_database(message):
    image_link = None
    caption = None

    # Mendapatkan link gambar (jika ada)
    if message.photo:
        image_link = message.photo.file_id

    # Mendapatkan caption teks
    if message.caption:
        caption = message.caption

    # Menyimpan ke database
    post = Post(image_link=image_link, caption=caption)
    db_session.add(post)
    db_session.commit()

# Handler untuk pesan dengan gambar dan caption dari channel tertentu
@app.on_message(filters.chat(channel_username) & filters.photo & filters.caption)
def handle_message(client, message):
    save_to_database(message)

# Jalankan bot
app.run()
