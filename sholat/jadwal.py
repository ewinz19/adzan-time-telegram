import os
import requests
from datetime import datetime

# ==============================
# 1. SETTINGS - SESUAIKAN INI!
# ==============================

try:
    with open(os.path.expanduser("~/ID_KOTA.txt"), 'r') as f:
        ID_KOTA = int(f.read().strip())
except (FileNotFoundError, ValueError):
    ID_KOTA = 2113  # Nilai defa
# ==============================
# 2. FUNGSI UTAMA
# ==============================
jam_sekarang = datetime.now().strftime("%H:%M")

def get_jadwal_hari_ini(id_kota):
    # Dapatkan tanggal hari ini dalam format YYYY-MM-DD
    tanggal_sekarang = datetime.now().strftime("%Y-%m-%d")
    # Buat URL endpoint harian
    url = f"https://api.myquran.com/v2/sholat/jadwal/{id_kota}/{tanggal_sekarang.replace('-', '/')}"
    
    try:
        # Lakukan request ke API
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # Cek status response
        if not data.get("status"):
            with open("sholat.txt", "w", encoding="utf-8") as f:
                f.write(f"Error dari API: {data.get('message', 'Unknown error')}\n")
            return None
        
        # Ambil data jadwal
        jadwal = data["data"]["jadwal"]
        
        # Cari sholat berikutnya terlebih dahulu
        sholat_berikutnya = cari_sholat_berikutnya(jadwal)
        
        # Format output untuk disimpan ke file sholat.txt
        output_lines = []

     # Tambahkan info sholat berikutnya di awal
        if sholat_berikutnya:
            nama, waktu = sholat_berikutnya
            output_lines.append(f"🕒  {waktu} {nama.upper()} Hampir Tiba")
            output_lines.append("="*28)

        
        # Lanjutkan dengan info jadwal lengkap
        output_lines.extend([
            f"╔{'═'*20}╗",
            f"║ 🕌 SHOLAT BERIKUTNYA 🕌     ",
            f"║     {nama.upper()} 🕒 {waktu}  ",
            f"╠{'═'*20}╣",
            f"║📍 {data['data']['lokasi']}  ",
            f"║  ({data['data']['daerah']}) ",
            f"║        {jadwal['tanggal']}  ",
            f"╚{'═'*20}╝",
            "="*28,
            f"🌙 Imsak     : {jadwal['imsak']}",
            f"🌄 Subuh    : {jadwal['subuh']}",
            f"☀️ Terbit     : {jadwal['terbit']}",
            f"🌤 Dhuha    : {jadwal['dhuha']}",
            f"☀️ Dzuhur   : {jadwal['dzuhur']}",
            f"🌥 Ashar     : {jadwal['ashar']}",
            f"🌇 Maghrib : {jadwal['maghrib']}",
            f"🌙 Isya        : {jadwal['isya']}",
            "="*28
        ])
        
        # Gabungkan semua baris output
        output = "\n".join(output_lines)
        
        # Simpan ke file sholat.txt (mode 'w' untuk menimpa file lama)
        with open("sholat.txt", "w", encoding="utf-8") as f:
            f.write(output + "\n")
        
        # Simpan info sholat berikutnya ke tiba.txt
        if sholat_berikutnya:
            nama, waktu = sholat_berikutnya
            with open("tiba.txt", "w", encoding="utf-8") as f:
                f.write(f"🕌WAKTU  SHOLAT TELAH SAMPAI\n")
                f.write(f"⏰ {nama.upper()} pukul {waktu}\n")
        
        return jadwal
        
    except requests.exceptions.RequestException as e:
        with open("sholat.txt", "w", encoding="utf-8") as f:
            f.write(f"Error koneksi: {e}\n")
    except ValueError as e:
        with open("sholat.txt", "w", encoding="utf-8") as f:
            f.write(f"Error parsing JSON: {e}\n")
    except KeyError as e:
        with open("sholat.txt", "w", encoding="utf-8") as f:
            f.write(f"Error struktur data tidak sesuai: {e}\n")
    
    return None

def cari_sholat_berikutnya(jadwal):
    """Mencari sholat berikutnya yang belum lewat"""
    sekarang = datetime.now().time()
    
    # Konversi waktu sholat dari string ke time object
    def parse_time(time_str):
        return datetime.strptime(time_str, "%H:%M").time()
    
    sholat_urutan = [
        ('Subuh', 'subuh'),
        ('Terbit', 'terbit'),
        ('Dhuha', 'dhuha'),
        ('Dzuhur', 'dzuhur'),
        ('Ashar', 'ashar'),
        ('Maghrib', 'maghrib'),
        ('Isya', 'isya')
    ]

    for nama, key in sholat_urutan:
        waktu_str = jadwal[key]
        waktu_sholat = parse_time(waktu_str)
        if waktu_sholat > sekarang:
            return nama, waktu_str

    # Jika semua sudah lewat, kembalikan sholat pertama besok (Subuh)
    return ('Subuh', jadwal['subuh'])

# ==============================
# 3. EKSEKUSI PROGRAM
# ==============================
if __name__ == "__main__":
    jadwal = get_jadwal_hari_ini(ID_KOTA)
