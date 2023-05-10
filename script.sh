#!/bin/bash

sudo docker build -t imagendata -f /home/ubuntu/Proyecto/df_db .
sudo docker run -t -d -p 8080:8080 --name dockerdb imagendata
sudo docker build -t imagenapi -f /home/ubuntu/Proyecto/df_api .
sudo docker run -t -d -p 8100:8100 --name dockerapi imagenapi
sudo docker build -t imagenfront -f /home/ubuntu/Proyecto/df_front .
sudo docker run -t -d -p 80:80 --name dockerfront imagenfront
