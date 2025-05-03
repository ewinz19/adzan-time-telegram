#!/bin/bash

TOKEN=$(cat "$HOME/sholat/.config/.tok" 2>/dev/null) || {
   echo error
  exit 1
}
API_URL="https://api.telegram.org/bot$TOKEN"
OFFSET=0

send_message() {
    curl -s -X POST "$API_URL/sendMessage" \
        -d "chat_id=$1" \
        -d "text=$2"
}

split_and_send() {
    local chat_id=$1
    local message=$2
    local CHUNK_SIZE=4000  # Batasi ukuran per pesan
    local LENGTH=${#message}

    # Kirim pesan dalam beberapa bagian jika melebihi batas
    for ((i=0; i<LENGTH; i+=CHUNK_SIZE)); do
        part="${message:i:CHUNK_SIZE}"
        send_message "$chat_id" "$part"
    done
}

while true; do
    RESPONSE=$(curl -s "$API_URL/getUpdates?offset=$((OFFSET + 1))&timeout=10")

    if [ -n "$RESPONSE" ]; then
        UPDATE_COUNT=$(echo "$RESPONSE" | jq '.result | length' 2>/dev/null || echo "0")

        for (( i=0; i<UPDATE_COUNT; i++ )); do
            UPDATE=$(echo "$RESPONSE" | jq ".result[$i]" 2>/dev/null || echo "")
            OFFSET=$(echo "$UPDATE" | jq ".update_id" 2>/dev/null || echo "$OFFSET")
            CHAT_ID=$(echo "$UPDATE" | jq ".message.chat.id" 2>/dev/null)
            TEXT=$(echo "$UPDATE" | jq -r ".message.text" 2>/dev/null)

            case "$TEXT" in
              "/start")
    FIRST_NAME=$(echo "$UPDATE" | jq -r ".message.from.first_name")
    LAST_NAME=$(echo "$UPDATE" | jq -r ".message.from.last_name // \"\"")
    USERNAME=$(echo "$UPDATE" | jq -r ".message.from.username // \"(tidak ada username)\"")
    USER_ID=$(echo "$UPDATE" | jq -r ".message.from.id")
    LANGUAGE=$(echo "$UPDATE" | jq -r ".message.from.language_code")
    DATE=$(date -d @"$(echo "$UPDATE" | jq -r ".message.date")" "+%d-%m-%Y %H:%M:%S")

    send_message "$CHAT_ID" "Halo $FIRST_NAME $LAST_NAME!
Username  : @$USERNAME
User ID   : $USER_ID
Bahasa    : $LANGUAGE
Waktu     : $DATE

Selamat datang di bot jadwal sholat!
Sumber data: https://api.myquran.com

Gunakan:
/list - Lihat kode daerah

/ <spasi> <kode daerah> -jadwal sholat Contoh: / 0232

===
"
    ;;


                

                "/list")
                    if [ ! -f "list.txt" ]; then
                        send_message "$CHAT_ID" "Error: File list.txt tidak ada"
                    else
                        OUTPUT=$(cat list.txt)
                        split_and_send "$CHAT_ID" "$OUTPUT"
                    fi
                    ;;

                /*)
                    KODE_DAERAH=$(echo "$TEXT" | awk '{print $2}')
                    
                    if [[ ! "$KODE_DAERAH" =~ ^[0-9]{4}$ ]]; then
                    echo  "$CHAT_ID" "Format kode salah. Contoh: /<spasi>0232"
                        continue
                    fi
                    
                    # Eksekusi script jadwal sholat
                    if [ ! -f "/root/sholat/data/sl.sh" ]; then
                     echo  "$CHAT_ID" "Error: Script sl.sh tidak ditemukan"
                    else
                        OUTPUT=$(./sl.sh "$KODE_DAERAH" 2>&1)
                        send_message "$CHAT_ID" "$OUTPUT"
                    fi
                    ;;

                *)
                echo  "$CHAT_ID" "Perintah tidak dikenali. Ketik /start untuk bantuan"
                    ;;
            esac
        done
    fi

    sleep 1
done

