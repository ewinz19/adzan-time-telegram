#!/bin/bash
clear
###diterbitkan selasa 13 april 2025 10:23 pm
HOME_DIR="$HOME/sholat"
WORK_TEMP="$HOME_DIR/sholat.txt"
python3 jadwal.py
sleep 1
clear

CHAT_ID=$(cat "$HOME/sholat/.config/.id" 2>/dev/null) || {
  echo error
    exit 1
}
TOKEN=$(cat "$HOME/sholat/.config/.tok" 2>/dev/null) || {
   echo error
  exit 1
}

MESSAGE=`cat $WORK_TEMP`
URL="https://api.telegram.org/bot$TOKEN/sendMessage"
for ID in "${CHAT_ID[@]}"
do
        curl -s -X POST $URL -d chat_id=$ID -d text="$MESSAGE";
done

