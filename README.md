

<p float="left">
  <img src="images/screenshot.jpg" width="400" />
  <img src="images/screenshot2.jpg" width="400" />
</p>

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





