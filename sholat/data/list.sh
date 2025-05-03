echo "kode daerah - nama wilayah" > list.txt
curl -s https://api.myquran.com/v2/sholat/kota/semua | jq -r '.data[] | "\(.id) \(.lokasi)"' >> list.txt
