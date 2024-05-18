#! /bin/bash

mkdir hping
mkdir slowloris

tar -zxf hping.tar.gz -C hping
tar -zxf slowloris.tar.gz -C slowloris

cd hping
for f in *.tar; do tar -xf "$f"; mv client_delay.csv ${f}.csv; done

cd ../slowloris
for f in *.tar; do tar -xf "$f"; mv client_delay.csv ${f}.csv; done

cd ..

python3 client_metrics.py hping
python3 client_metrics.py slowloris

rm -rf hping
rm -rf slowloris