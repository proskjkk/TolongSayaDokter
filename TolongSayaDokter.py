from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler,ContextTypes, filters
from datetime import datetime
import json

TOKEN = '7483315349:AAFX4zQdLgULcIrX8hOMJq2wdKUymWZ6qU4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Selamat Datang di TolongSayaDokter\n ketik /bantuan untuk memulai")

async def halo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if update.message.text.lower() == "halo":
        await update.message.reply_text("Hai juga! 👋")
    elif update.message.text.lower() == "siapa kamu":
        await update.message.reply_text("Saya adalah bot yang akan membantu kamu untuk mengenali beberapa penyakit yang kamu alami!")
    elif update.message.text.lower() == "confs":
        await update.message.reply_text("Saya Senang kamu disini")
    else:
        await update.message.reply_text("perintah tidak dikenali")
    LogUser(update.message.text, update.message.chat.first_name, update.message.chat.last_name)
    print(user)

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = (
        "Ini daftar perintah yang bisa kamu coba:\n"
        "/start - Mulai chat dengan bot\n"
        "/bantuan - Tampilkan daftar perintah\n"
        "halo - Sapa bot\n"
        "Secret - Guess the Command\n"
    )
    await update.message.reply_text(pesan)

def LogUser(HistoryChat, first_name, last_name):
    with open("Log.txt", "a") as file:
        a = file.write(HistoryChat + " | " + first_name + " " + last_name +'\n')

def cek_gejala(gejala_user, data_penyakit):
    # PERBAIKAN: Cek apakah input string atau list
    if isinstance(gejala_user, str):
        # Jika string, pisahkan berdasarkan koma
        if ',' in gejala_user:
            gejala_user = [g.strip() for g in gejala_user.split(',')]
        else:
            # Jika tidak ada koma, anggap sebagai satu gejala
            gejala_user = [gejala_user.strip()]
    """Fungsi untuk cek gejala user dengan database penyakit"""
    # Ubah input user jadi huruf kecil
    gejala_user_bersih = []
    for gejala in gejala_user:
        gejala_bersih = gejala.lower().strip()
        gejala_user_bersih.append(gejala_bersih)
    
    # Cari penyakit yang cocok
    hasil = []
    
    for penyakit in data_penyakit:
        nama_penyakit = penyakit["nama"]
        gejala_penyakit = penyakit["gejala"]
        saran = penyakit["saran"]
        
        # Hitung berapa gejala yang sama
        cocok = 0
        for gejala in gejala_user_bersih:
            if gejala in gejala_penyakit:
                cocok += 1
        
        # Simpan hasil jika ada yang cocok
        if cocok > 0:
            hasil.append({
                "nama": nama_penyakit,
                "cocok": cocok,
                "saran" : saran
            })
    
    # Cari yang paling cocok
    if len(hasil) == 0:
        return "Sebaiknya konsultasi dokter"
    
    # Urutkan dari yang paling cocok
    hasil_urut = sorted(hasil, key=lambda x: x["cocok"], reverse=True)
    penyakit_terbaik = hasil_urut[0]
    
    nama = penyakit_terbaik["nama"]
    saran_a = penyakit_terbaik["saran"]
    jumlah_cocok = penyakit_terbaik["cocok"]
    
    # Tentukan tingkat keyakinan
    if jumlah_cocok >= 3:
        # return f"Kemungkinan besar {nama}, {saran_a}"
        response = f"Kemungkinan besar {nama}, {saran_a}"
    elif jumlah_cocok == 2:
        # return f"Mungkin {nama}, {saran_a}"
        response = f"Mungkin {nama}, {saran_a}"
    elif jumlah_cocok == 1:
        # return f"Kemungkinan kecil {nama}, {saran_a}"
        response = f"Kemungkinan kecil {nama}, {saran_a}"
    return response

async def diagnosa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("penyakit.json", "r") as file:
        data = json.load(file)
    hasil = cek_gejala(context.args, data["database_penyakit"])
    await update.message.reply_text(hasil)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("bantuan", bantuan))
app.add_handler(CommandHandler("diagnosa", diagnosa_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, halo_handler))

print("Bot Sudah Berjalan!!")
app.run_polling()