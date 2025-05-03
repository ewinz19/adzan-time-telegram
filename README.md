
![Screenshot](images/screenshot2.jpg)



####  ####  ####
#install server pengingat waktu telegram INDONESIA 
#
mv adzan-time-telegram/sholat $HOME/

bash sholat/install.sh.wal

#token_bot telegram

nano sholat/.config/.id

#id supergrup

nano sholat/.config/.tok
systemctl start sholat-bot

#masukan id kota cek chat private bot
nano sholat/ID_KOTA.txt

systemctl start sholat-sebelum

systemctl start sholat-tiba

systemctl status sholat-bot sholat-sebelum sholat-tiba






![Screenshot](images/screenshot.jpg)
