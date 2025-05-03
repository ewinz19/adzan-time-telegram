#!/bin/bash

clear
sleep 60   #waktu tiba tunda 1 menit dari sumber api .anda bisa atur sendiri
###diterbitkan selasa 13 april 2025 10:23 pm
HOME_DIR="$HOME/sholat"
WORK_TEMP="$HOME_DIR/tiba.txt"
CHAT_ID=$(cat "$HOME/sholat/.config/.id" 2>/dev/null) || {
  echo error
    exit 1
}
TOKEN=$(cat "$HOME/sholat/.config/.tok" 2>/dev/null) || {
   echo error  
  exit 1
}
sleep 1
MESSAGE=`cat $WORK_TEMP`
URL="https://api.telegram.org/bot$TOKEN/sendMessage"
for ID in "${CHAT_ID[@]}"
do
        curl -s -X POST $URL -d chat_id=$ID -d text="$MESSAGE";
done
