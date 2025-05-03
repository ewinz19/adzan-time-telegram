-----BOT TELEGRAM WAKTU SHOLAT INDONESIA-------

#############source https://api.myquran.com #######

<p float="left">
  <img src="images/Screenshot.jpg" width="400" />
  <img src="images/Screenshot2.jpg" width="400" />
</p>

##Cara INSTALL
#install server pengingat waktu telegram INDONESIA 
#silakan copas

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




#saran untuk pengingat waktu kita bisa mengatur nada dering grup
sesuai keinginan kita dan ment aktip kan mode pop up
