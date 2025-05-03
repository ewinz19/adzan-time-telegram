import requests
from datetime import datetime

# by ewinz 26 Maret 2025

idd = input("by ewinz source https://api.myquran.com ")
ID_KOTA = idd

jam_sekarang = datetime.now().strftime("%H:%M")

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

        jadwal = data["data"]["jadwal"]
        tanggal = jadwal["tanggal"]

        print(f"\n📆 Jadwal Sholat - {tanggal}")
        print(f"⏰ Waktu sekarang : {jam_sekarang}")
        print(f"📍 Lokasi         : {data['data']['lokasi']}")
        print(f"🗺️  Daerah         : {data['data']['daerah']}\n")

        print(f"🌙  {'Imsak':<9}: {jadwal['imsak']}")
        print(f"🌄  {'Subuh':<9}: {jadwal['subuh']}")
        print(f"☀️  {'Terbit':<11}: {jadwal['terbit']}")
        print(f"🌤  {'Dhuha':<9}: {jadwal['dhuha']}")
        print(f"🏞️  {'Dzuhur':<9}: {jadwal['dzuhur']}")
        print(f"🌥  {'Ashar':<10}: {jadwal['ashar']}")
        print(f"🌇  {'Maghrib':<8}: {jadwal['maghrib']}")
        print(f"🌌  {'Isya':<13}: {jadwal['isya']}\n")

        return jadwal

    except requests.exceptions.RequestException as e:
        print(f"Error koneksi: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
    except KeyError as e:
        print(f"Error struktur data tidak sesuai: {e}")

    return None

def cari_sholat_berikutnya(jadwal):
    sekarang = datetime.now().time()

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

    return ('Subuh (Besok)', jadwal['subuh'])

if __name__ == "__main__":
    jadwal = get_jadwal_hari_ini(ID_KOTA)
    if jadwal:
        sholat_berikutnya = cari_sholat_berikutnya(jadwal)

        if sholat_berikutnya:
            nama, waktu = sholat_berikutnya
            print(f"🕌 Sholat berikutnya: {nama} pukul {waktu}")
        else:
            print("ℹ️ Semua jadwal sholat hari ini sudah selesai")

