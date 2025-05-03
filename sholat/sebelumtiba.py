import requests
from datetime import datetime, timedelta
import time
import subprocess
import os

# ==============================
# 1. SETTINGS -
# ==============================
#ID_KOTA = 2104  # Ganti dengan ID kota Anda

# Coba baca dari file, jika tidak ada gunakan default
try:
    with open(os.path.expanduser("/root/sholat/ID_KOTA.txt"), 'r') as f:
        ID_KOTA = int(f.read().strip())
except (FileNotFoundError, ValueError):
    ID_KOTA = 2104  # Nilai default


BASH_SCRIPT = "/root/sholat/jadwal.sh"  # Path ke script bash Anda
CHECK_INTERVAL = 30  # Interval pengecekan dalam detik (30 = setengah menit)
NOTIFY_BEFORE = 10  # Menit sebelum waktu sholat untuk eksekusi

# ==============================
# 2. FUNGSI UTAMA
# ==============================
def get_jadwal_hari_ini(id_kota):
    tanggal_sekarang = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.myquran.com/v2/sholat/jadwal/{id_kota}/{tanggal_sekarang.replace('-', '/')}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("status"):
            print(f"Error dari API: {data.get('message', 'Unknown error')}")
            return None
        
        return data["data"]["jadwal"]
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

def jalankan_bash_script():
    try:
        if os.path.exists(BASH_SCRIPT):
            subprocess.run(["bash", BASH_SCRIPT], check=True)
            print(f"[EKSEKUSI] Script {BASH_SCRIPT} berhasil dijalankan")
        else:
            print(f"[ERROR] File {BASH_SCRIPT} tidak ditemukan")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Gagal menjalankan script: {e}")

# ==============================
# 3. EKSEKUSI PROGRAM
# ==============================
def main():
    print("=== Program Pengingat Sholat 5 Menit Sebelum Waktu ===")
    print(f"Memeriksa setiap {CHECK_INTERVAL} detik\n")
    
    terakhir_dijalankan = {}
    jadwal_sekarang = None
    
    while True:
        sekarang = datetime.now()
        tanggal_hari_ini = sekarang.strftime("%Y-%m-%d")
        
        # Ambil jadwal baru setiap hari
        if jadwal_sekarang is None or jadwal_sekarang.get('tanggal') != tanggal_hari_ini:
            print(f"\n[{sekarang}] Memperbarui jadwal sholat...")
            jadwal_sekarang = get_jadwal_hari_ini(ID_KOTA)
            if not jadwal_sekarang:
                print("[ERROR] Gagal mendapatkan jadwal sholat")
                time.sleep(CHECK_INTERVAL)
                continue
        
        # Daftar waktu sholat utama
        sholat_times = {
            'Subuh': jadwal_sekarang['subuh'],
            'Dzuhur': jadwal_sekarang['dzuhur'],
            'Ashar': jadwal_sekarang['ashar'],
            'Maghrib': jadwal_sekarang['maghrib'],
            'Isya': jadwal_sekarang['isya']
        }
        
        for nama, waktu_str in sholat_times.items():
            waktu_sholat = datetime.combine(sekarang.date(), parse_time(waktu_str))
            waktu_eksekusi = waktu_sholat - timedelta(minutes=NOTIFY_BEFORE)
            key = f"{nama}_{waktu_str}"  # Define key here
            
            # Cek jika sudah waktunya eksekusi
            if sekarang >= waktu_eksekusi and waktu_sholat > sekarang:
                if key not in terakhir_dijalankan:
                    print(f"\n[{sekarang}] Akan {nama} pukul {waktu_str}")
                    print(f"[{sekarang}] Menjalankan peringatan 5 menit sebelum {nama}...")
                    jalankan_bash_script()
                    terakhir_dijalankan[key] = True
            # Reset status jika sudah lewat waktu sholat
            elif sekarang > waktu_sholat and key in terakhir_dijalankan:
                terakhir_dijalankan.pop(key, None)
        
        print(f"[{sekarang.strftime('%H:%M:%S')}] Memantau...", end='\r')
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
