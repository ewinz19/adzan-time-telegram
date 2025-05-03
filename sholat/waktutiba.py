#!/usr/bin/env python3
import requests
import time
import subprocess
import os
import json
from datetime import datetime

# ==============================
# 1. PENGATURAN (CUSTOMIZE)
# ==============================

try:
    with open(os.path.expanduser("/root/sholat/ID_KOTA.txt"), 'r') as f:
        ID_KOTA = f.read().strip()
except (FileNotFoundError, ValueError):
    ID_KOTA = 2113 # Nilai default

BASH_SCRIPT      = "/root/sholat/tiba.sh"
CHECK_INTERVAL   = 30    # detik
STATUS_FILE      = "/root/sholat/last_run_status.json"
JADWAL_CACHE     = "/root/sholat/jadwal_today.json"

# ==============================
# 2. HELPERS: STATUS & CACHE
# ==============================
def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, path)

def load_status():
    # struktur: { "date": "YYYY-MM-DD", "times": [ "HH:MM", ... ] }
    return load_json(STATUS_FILE, {"date": None, "times": []})

def save_status(st):
    save_json(STATUS_FILE, st)

def load_jadwal_cache():
    # struktur cache: { "date": "YYYY-MM-DD", "jadwal": { subuh, dzuhur, ... } }
    return load_json(JADWAL_CACHE, {"date": None, "jadwal": None})

def save_jadwal_cache(date, jadwal):
    save_json(JADWAL_CACHE, {"date": date, "jadwal": jadwal})

# ==============================
# 3. FUNGSI UTILITY
# ==============================
def get_jadwal_hari_ini(id_kota):
    tgl = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.myquran.com/v2/sholat/jadwal/{id_kota}/{tgl.replace('-','/')}"
    resp = requests.get(url); resp.raise_for_status()
    data = resp.json()
    if not data.get("status"):
        raise RuntimeError(f"API error: {data.get('message')}")
    return data["data"]["jadwal"]

def waktu_sholat_datang(jadwal):
    now = datetime.now().strftime("%H:%M")
    times = [jadwal[k].strip() for k in ("subuh","dzuhur","ashar","maghrib","isya")]
    return now if now in times else None

def jalankan_script():
    if os.path.isfile(BASH_SCRIPT) and os.access(BASH_SCRIPT, os.X_OK):
        subprocess.run([BASH_SCRIPT], check=True)
    else:
        print(f"[ERROR] '{BASH_SCRIPT}' tidak ditemukan atau tidak executable")

# ==============================
# 4. MAIN LOOP
# ==============================
def main():
    print("=== Penjadwal Adzan Started ===")
    status = load_status()
    cache  = load_jadwal_cache()

    while True:
        try:
            today = datetime.now().strftime("%Y-%m-%d")

            # — jika hari baru atau cache jadwal kosong/tidak cocok, refresh keduanya
            if cache["date"] != today:
                status = {"date": today, "times": []}
                save_status(status)

                jadwal = get_jadwal_hari_ini(ID_KOTA)
                cache = {"date": today, "jadwal": jadwal}
                save_jadwal_cache(today, jadwal)
                print(f"[{today}] Jadwal baru diambil: {jadwal}")

            else:
                jadwal = cache["jadwal"]

            # cek trigger adzan
            w = waktu_sholat_datang(jadwal)
            if w and w not in status["times"]:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{ts}] Waktu sholat {w} tiba → menjalankan bash")
                jalankan_script()
                status["times"].append(w)
                save_status(status)

        except Exception as e:
            print(f"[WARN] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} – {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
