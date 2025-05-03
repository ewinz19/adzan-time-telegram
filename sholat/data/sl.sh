#!/bin/bash
# sl.sh - wrapper untuk sholat.py yang menerima argument
export LC_ALL=C.UTF-8
export PYTHONIOENCODING=utf-8

KODE_DAERAH=$1  # Ambil kode daerah dari parameter pertama

# Simulasikan input user menggunakan pipe
echo "$KODE_DAERAH" | python3 /root/sholat/data/sl.py


#python3 sholat.py


